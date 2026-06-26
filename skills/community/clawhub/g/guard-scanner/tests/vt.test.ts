import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
/**
 * guard-scanner VirusTotal統合テストスイート
 *
 * node --test で実行
 * mock _httpGetを使い外部APIアクセスなしでテスト
 */

import { expect, describe, it, assert, beforeEach, afterEach, vi } from 'vitest';

import path  from 'path';
import fs  from 'fs';
import crypto  from 'crypto';
import { VTClient, VT_API_BASE, VT_RATE_LIMIT  } from '../src/vt-client';

// ===== Mock VT API Responses =====
const MOCK_VT_FILE_CLEAN = {
    found: true,
    data: {
        data: {
            attributes: {
                last_analysis_stats: { malicious: 0, suspicious: 0, harmless: 60, undetected: 10 },
                last_analysis_results: {},
                reputation: 0,
                tags: [],
            },
        },
    },
};

const MOCK_VT_FILE_MALICIOUS = {
    found: true,
    data: {
        data: {
            attributes: {
                last_analysis_stats: { malicious: 45, suspicious: 3, harmless: 12, undetected: 10 },
                last_analysis_results: {
                    'CrowdStrike': { category: 'malicious', result: 'Trojan.GenericKD' },
                    'Kaspersky': { category: 'malicious', result: 'HEUR:Trojan.Script.Agent' },
                    'Bitdefender': { category: 'malicious', result: 'Trojan.GenericKD.47659' },
                    'ESET-NOD32': { category: 'suspicious', result: 'JS/Agent.NQR' },
                },
                reputation: -85,
                tags: ['trojan', 'javascript'],
            },
        },
    },
};

const MOCK_VT_URL_MALICIOUS = {
    found: true,
    data: {
        data: {
            attributes: {
                last_analysis_stats: { malicious: 12, suspicious: 2, harmless: 50 },
                categories: { 'Forcepoint ThreatSeeker': 'malicious' },
            },
        },
    },
};

const MOCK_VT_DOMAIN_MALICIOUS = {
    found: true,
    data: {
        data: {
            attributes: {
                reputation: -70,
                last_analysis_stats: { malicious: 8, suspicious: 1 },
                categories: { 'BitDefender': 'phishing' },
                registrar: 'Namecheap Inc.',
            },
        },
    },
};

const MOCK_VT_IP_MALICIOUS = {
    found: true,
    data: {
        data: {
            attributes: {
                reputation: -50,
                last_analysis_stats: { malicious: 5, suspicious: 2 },
                country: 'RU',
                as_owner: 'Suspicious Hosting LLC',
            },
        },
    },
};

// ===== Mock httpGet =====
function createMockVTGet(responses = {}) {
    return async (url) => {
        for (const [pattern, response] of Object.entries(responses)) {
            if (url.includes(pattern)) {
                if (response instanceof Error) throw response;
                return response;
            }
        }
        return { found: false, data: null };
    };
}

// ===== 1. VTClient Construction =====
describe('VTClient: Construction', () => {
    it('should require API key', () => {
        assert.throws(() => new VTClient(''), /API key is required/);
        assert.throws(() => new VTClient(null), /API key is required/);
    });

    it('should accept valid API key', () => {
        const client = new VTClient('test-api-key-123');
        assert.ok(client);
        assert.equal(client.apiKey, 'test-api-key-123');
    });

    it('should export constants', () => {
        assert.ok(VT_API_BASE.includes('virustotal.com'));
        assert.equal(VT_RATE_LIMIT, 4);
    });
});

// ===== 2. Hash Lookup =====
describe('VTClient: Hash Lookup', () => {
    it('should detect malicious file by hash', async () => {
        const client = new VTClient('test-key', {
            _httpGet: createMockVTGet({ '/files/': MOCK_VT_FILE_MALICIOUS }),
        });
        const result = await client.lookupHash('a'.repeat(64));
        assert.equal(result.found, true);
        assert.equal(result.malicious, 45);
        assert.ok(result.engines['CrowdStrike']);
        assert.ok(result.engines['Kaspersky']);
    });

    it('should report clean file', async () => {
        const client = new VTClient('test-key', {
            _httpGet: createMockVTGet({ '/files/': MOCK_VT_FILE_CLEAN }),
        });
        const result = await client.lookupHash('b'.repeat(64));
        assert.equal(result.found, true);
        assert.equal(result.malicious, 0);
        assert.equal(Object.keys(result.engines).length, 0);
    });

    it('should handle unknown hash', async () => {
        const client = new VTClient('test-key', {
            _httpGet: createMockVTGet({}), // returns { found: false }
        });
        const result = await client.lookupHash('c'.repeat(64));
        assert.equal(result.found, false);
        assert.equal(result.malicious, 0);
    });

    it('should reject invalid hash', async () => {
        const client = new VTClient('test-key', { _httpGet: createMockVTGet({}) });
        await await expect(client.lookupHash('short')).rejects.toThrow(/Invalid hash/);
    });

    it('should handle API errors', async () => {
        const client = new VTClient('test-key', {
            _httpGet: createMockVTGet({ '/files/': new Error('Network error') }),
        });
        await await expect(client.lookupHash('d'.repeat(64))).rejects.toThrow(/Network error/);
    });
});

// ===== 3. URL Scan =====
describe('VTClient: URL Scan', () => {
    it('should detect malicious URL', async () => {
        const client = new VTClient('test-key', {
            _httpGet: createMockVTGet({ '/urls/': MOCK_VT_URL_MALICIOUS }),
        });
        const result = await client.scanURL('https://evil.com/malware');
        assert.equal(result.found, true);
        assert.equal(result.malicious, 12);
    });

    it('should handle unknown URL', async () => {
        const client = new VTClient('test-key', { _httpGet: createMockVTGet({}) });
        const result = await client.scanURL('https://clean.example.com');
        assert.equal(result.found, false);
    });

    it('should require URL', async () => {
        const client = new VTClient('test-key', { _httpGet: createMockVTGet({}) });
        await await expect(client.scanURL('')).rejects.toThrow(/URL is required/);
    });
});

// ===== 4. Domain Report =====
describe('VTClient: Domain Report', () => {
    it('should detect malicious domain', async () => {
        const client = new VTClient('test-key', {
            _httpGet: createMockVTGet({ '/domains/': MOCK_VT_DOMAIN_MALICIOUS }),
        });
        const result = await client.checkDomain('evil.example.com');
        assert.equal(result.found, true);
        assert.equal(result.reputation, -70);
        assert.equal(result.malicious, 8);
    });

    it('should require domain', async () => {
        const client = new VTClient('test-key', { _httpGet: createMockVTGet({}) });
        await await expect(client.checkDomain('')).rejects.toThrow(/Domain is required/);
    });
});

// ===== 5. IP Report =====
describe('VTClient: IP Report', () => {
    it('should detect malicious IP', async () => {
        const client = new VTClient('test-key', {
            _httpGet: createMockVTGet({ '/ip_addresses/': MOCK_VT_IP_MALICIOUS }),
        });
        const result = await client.checkIP('91.92.242.30');
        assert.equal(result.found, true);
        assert.equal(result.malicious, 5);
        assert.equal(result.country, 'RU');
    });

    it('should require IP', async () => {
        const client = new VTClient('test-key', { _httpGet: createMockVTGet({}) });
        await await expect(client.checkIP('')).rejects.toThrow(/IP address is required/);
    });
});

// ===== 6. Rate Limiting =====
describe('VTClient: Rate Limiting', () => {
    it('should track request count', async () => {
        const client = new VTClient('test-key', {
            _httpGet: createMockVTGet({ '/files/': MOCK_VT_FILE_CLEAN }),
        });
        await client.lookupHash('a'.repeat(64));
        assert.equal(client._requestCount, 1);
        await client.lookupHash('b'.repeat(64));
        assert.equal(client._requestCount, 2);
    });

    it('should reset counter after 60s window', async () => {
        const client = new VTClient('test-key', {
            _httpGet: createMockVTGet({ '/files/': MOCK_VT_FILE_CLEAN }),
        });
        client._requestCount = 3;
        client._windowStart = Date.now() - 61000; // 61 seconds ago
        await client.lookupHash('e'.repeat(64));
        assert.equal(client._requestCount, 1); // reset + 1
    });
});

// ===== 7. File Hashing =====
describe('VTClient: File Hashing', () => {
    it('should compute SHA256 of file', () => {
        const tmpFile = path.join(__dirname, '__test_hash_file.tmp');
        fs.writeFileSync(tmpFile, 'test content for hashing');
        try {
            const hash = VTClient.hashFile(tmpFile);
            const expected = crypto.createHash('sha256').update('test content for hashing').digest('hex');
            assert.equal(hash, expected);
            assert.equal(hash.length, 64);
        } finally {
            fs.unlinkSync(tmpFile);
        }
    });
});

// ===== 8. Integration with Asset Auditor =====
describe('VTClient: Integration Patterns', () => {
    it('should work with IoC DB known IPs', async () => {
        const client = new VTClient('test-key', {
            _httpGet: createMockVTGet({ '/ip_addresses/': MOCK_VT_IP_MALICIOUS }),
        });
        // 91.92.242.30 is ClawHavoc C2 from our IoC DB
        const result = await client.checkIP('91.92.242.30');
        assert.ok(result.found);
        assert.ok(result.malicious > 0, 'Known C2 IP should be flagged');
    });

    it('should work with IoC DB known domains', async () => {
        const client = new VTClient('test-key', {
            _httpGet: createMockVTGet({ '/domains/': MOCK_VT_DOMAIN_MALICIOUS }),
        });
        const result = await client.checkDomain('webhook.site');
        assert.ok(result.found);
    });
});
