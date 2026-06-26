import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { extractDomains } from '../src/extract.js';
import type { DiscoveredFile } from '../src/types.js';

describe('extractDomains — domain extraction', () => {
  // ── 1. URL literal (1 test) ───────────────────────────────────────────

  it('extracts domain from an HTTP URL literal', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/api.ts',
      content: 'const endpoint = "https://api.example.com/v1/data";',
    }];
    const domains = extractDomains(files);
    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'api.example.com');
    assert.equal(domains[0]!.scheme, 'https');
  });

  // ── 2. fetch / HTTP-client calls (2 tests) ───────────────────────────

  it('extracts domain from fetch call with string URL', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/client.ts',
      content: 'const res = await fetch("https://gateway.service.io/submit");',
    }];
    const domains = extractDomains(files);
    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'gateway.service.io');
  });

  it('extracts domain from axios options object with baseURL', () => {
    const files: DiscoveredFile[] = [{
      path: 'src/http.ts',
      content: [
        'const client = axios.create({',
        '  baseURL: "https://cdn.assets.io/v2",',
        '  timeout: 5000,',
        '});',
      ].join('\n'),
    }];
    const domains = extractDomains(files);
    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'cdn.assets.io');
  });

  // ── 3. Config-embedded domains (3 tests) ──────────────────────────────

  it('extracts bare domain from JSON config with Host key', () => {
    const files: DiscoveredFile[] = [{
      path: 'config/proxy.json',
      content: JSON.stringify({
        proxy: { Host: 'db.primary.internal' },
      }, null, 2),
    }];
    const domains = extractDomains(files);
    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'db.primary.internal');
    assert.equal(domains[0]!.scheme, 'https');
  });

  it('extracts domain from YAML-style config with baseUrl value', () => {
    const files: DiscoveredFile[] = [{
      path: 'config/services.yml',
      content: [
        'service:',
        '  name: payments',
        '  baseUrl: "https://api.staging.example.com/v3"',
        '  retries: 3',
      ].join('\n'),
    }];
    const domains = extractDomains(files);
    assert.equal(domains.length, 1);
    assert.equal(domains[0]!.hostname, 'api.staging.example.com');
  });

  it('extracts domains from nested config with non-obvious keys', () => {
    const files: DiscoveredFile[] = [{
      path: 'config/infra.json',
      content: JSON.stringify({
        services: {
          registry: 'https://registry.npmjs.org',
          server: 'https://auth.company.io/oauth',
          endpoint: 'https://reporting.analytics.io/v2',
        },
      }, null, 2),
    }];
    const domains = extractDomains(files);
    const hostnames = domains.map(d => d.hostname).sort();
    assert.deepEqual(hostnames, [
      'auth.company.io',
      'registry.npmjs.org',
      'reporting.analytics.io',
    ]);
  });
});
