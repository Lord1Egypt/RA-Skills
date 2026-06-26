// @ts-nocheck
/**
 * guard-scanner v7 — VirusTotal API v3 Client
 *
 * @security-manifest
 *   env-read: [VT_API_KEY]
 *   env-write: []
 *   network: [virustotal.com API v3]
 *   fs-read: [files for SHA256 hashing]
 *   fs-write: []
 *   exec: none
 *   purpose: VirusTotal threat intelligence integration
 */

import https  from 'https';
import crypto  from 'crypto';
import fs  from 'fs';

const VT_API_BASE = 'https://www.virustotal.com/api/v3';
const VT_RATE_LIMIT = 4; // requests per minute (free tier)

class VTClient {
    constructor(apiKey, options = {}) {
        if (!apiKey) throw new Error('VirusTotal API key is required. Set VT_API_KEY environment variable.');
        this.apiKey = apiKey;
        this.timeout = options.timeout || 15000;
        this.verbose = options.verbose || false;
        this._requestCount = 0;
        this._windowStart = Date.now();
        this._httpGet = options._httpGet || null; // DI for testing
        this._httpPost = options._httpPost || null;
    }

    // ── Rate limiter (4 req/min free tier) ──────────────────────
    async _throttle() {
        const now = Date.now();
        const elapsed = now - this._windowStart;
        if (elapsed >= 60000) {
            this._requestCount = 0;
            this._windowStart = now;
        }
        if (this._requestCount >= VT_RATE_LIMIT) {
            const waitMs = 60000 - elapsed + 100;
            if (this.verbose) console.log(`⏳ VT rate limit: waiting ${Math.ceil(waitMs / 1000)}s`);
            await new Promise(r => setTimeout(r, waitMs));
            this._requestCount = 0;
            this._windowStart = Date.now();
        }
        this._requestCount++;
    }

    // ── HTTP helpers ────────────────────────────────────────────
    async _get(path) {
        await this._throttle();
        if (this._httpGet) return this._httpGet(`${VT_API_BASE}${path}`);

        return new Promise((resolve, reject) => {
            const req = https.request({
                hostname: 'www.virustotal.com',
                path: `/api/v3${path}`,
                method: 'GET',
                headers: {
                    'x-apikey': this.apiKey,
                    'Accept': 'application/json',
                },
            }, (res) => {
                let data = '';
                res.on('data', chunk => { data += chunk; });
                res.on('end', () => {
                    try {
                        const parsed = JSON.parse(data);
                        if (res.statusCode === 429) {
                            reject(new Error('VT rate limit exceeded'));
                        } else if (res.statusCode === 404) {
                            resolve({ found: false, data: null });
                        } else if (res.statusCode >= 200 && res.statusCode < 300) {
                            resolve({ found: true, data: parsed });
                        } else {
                            reject(new Error(`VT API error ${res.statusCode}: ${JSON.stringify(parsed).substring(0, 200)}`));
                        }
                    } catch (e) {
                        reject(new Error(`VT response parse error: ${e.message}`));
                    }
                });
            });
            req.on('error', reject);
            req.setTimeout(this.timeout, () => { req.destroy(); reject(new Error('VT API timeout')); });
            req.end();
        });
    }

    // ── File Hash Lookup ───────────────────────────────────────
    async lookupHash(hash) {
        if (!hash || hash.length < 32) throw new Error('Invalid hash: provide MD5, SHA1, or SHA256');
        const result = await this._get(`/files/${hash}`);

        if (!result.found) {
            return { found: false, hash, malicious: 0, suspicious: 0, harmless: 0, undetected: 0, engines: {} };
        }

        const attrs = result.data.data?.attributes || {};
        const stats = attrs.last_analysis_stats || {};
        const results = attrs.last_analysis_results || {};

        // Extract detected engines
        const detectedEngines = {};
        for (const [engine, info] of Object.entries(results)) {
            if (info.category === 'malicious' || info.category === 'suspicious') {
                detectedEngines[engine] = { category: info.category, result: info.result };
            }
        }

        return {
            found: true,
            hash,
            malicious: stats.malicious || 0,
            suspicious: stats.suspicious || 0,
            harmless: stats.harmless || 0,
            undetected: stats.undetected || 0,
            engines: detectedEngines,
            reputation: attrs.reputation || 0,
            tags: attrs.tags || [],
        };
    }

    // ── URL Scan ───────────────────────────────────────────────
    async scanURL(url) {
        if (!url) throw new Error('URL is required');
        // URL ID = base64url of the URL
        const urlId = Buffer.from(url).toString('base64').replace(/=/g, '').replace(/\+/g, '-').replace(/\//g, '_');
        const result = await this._get(`/urls/${urlId}`);

        if (!result.found) {
            return { found: false, url, malicious: 0, suspicious: 0, harmless: 0 };
        }

        const attrs = result.data.data?.attributes || {};
        const stats = attrs.last_analysis_stats || {};

        return {
            found: true,
            url,
            malicious: stats.malicious || 0,
            suspicious: stats.suspicious || 0,
            harmless: stats.harmless || 0,
            categories: attrs.categories || {},
        };
    }

    // ── Domain Report ──────────────────────────────────────────
    async checkDomain(domain) {
        if (!domain) throw new Error('Domain is required');
        const result = await this._get(`/domains/${domain}`);

        if (!result.found) {
            return { found: false, domain, reputation: 0, malicious: 0 };
        }

        const attrs = result.data.data?.attributes || {};
        const stats = attrs.last_analysis_stats || {};

        return {
            found: true,
            domain,
            reputation: attrs.reputation || 0,
            malicious: stats.malicious || 0,
            suspicious: stats.suspicious || 0,
            categories: attrs.categories || {},
            registrar: attrs.registrar || 'unknown',
        };
    }

    // ── IP Report ──────────────────────────────────────────────
    async checkIP(ip) {
        if (!ip) throw new Error('IP address is required');
        const result = await this._get(`/ip_addresses/${ip}`);

        if (!result.found) {
            return { found: false, ip, reputation: 0, malicious: 0 };
        }

        const attrs = result.data.data?.attributes || {};
        const stats = attrs.last_analysis_stats || {};

        return {
            found: true,
            ip,
            reputation: attrs.reputation || 0,
            malicious: stats.malicious || 0,
            suspicious: stats.suspicious || 0,
            country: attrs.country || 'unknown',
            as_owner: attrs.as_owner || 'unknown',
        };
    }

    // ── File SHA256 helper ──────────────────────────────────────
    static hashFile(filePath) {
        const content = fs.readFileSync(filePath);
        return crypto.createHash('sha256').update(content).digest('hex');
    }
}

export {  VTClient, VT_API_BASE, VT_RATE_LIMIT  };
