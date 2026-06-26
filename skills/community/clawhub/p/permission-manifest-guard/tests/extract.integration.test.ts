import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { extractDomains } from '../src/index.js';
import type { Domain, DiscoveredFile } from '../src/index.js';

/**
 * Integration tests for extractDomains — verifies barrel export,
 * URL extraction, bare-hostname extraction, deduplication, localhost
 * filtering, file-URI exclusion, and multi-format config scanning.
 */

/** Helper: build a DiscoveredFile from path and content lines. */
function file(path: string, lines: string[]): DiscoveredFile {
  return { path, content: lines.join('\n') };
}

describe('extractDomains integration', () => {
  // -----------------------------------------------------------------------
  // 1. Standard URL extraction (http, https, ws, wss)
  // -----------------------------------------------------------------------
  it('extracts http, https, ws, and wss URLs from source files', () => {
    const files: DiscoveredFile[] = [
      file('src/client.ts', [
        'const API = "https://api.example.com/v1/users";',
        'const WS  = "wss://stream.example.com:8080/events";',
        'const LEGACY = "http://old.example.com";',
        'const INSECURE_WS = "ws://live.example.com/feed";',
      ]),
    ];

    const domains = extractDomains(files);

    const hostnames = domains.map(d => d.hostname);
    assert.ok(hostnames.includes('api.example.com'), 'should extract https URL');
    assert.ok(hostnames.includes('stream.example.com'), 'should extract wss URL');
    assert.ok(hostnames.includes('old.example.com'), 'should extract http URL');
    assert.ok(hostnames.includes('live.example.com'), 'should extract ws URL');

    const wss = domains.find(d => d.hostname === 'stream.example.com')!;
    assert.equal(wss.scheme, 'wss');
    assert.equal(wss.port, 8080);
    assert.equal(wss.sourceFile, 'src/client.ts');
    assert.equal(wss.line, 2);
    assert.ok(wss.context.length > 0, 'should include a context snippet');

    const https = domains.find(d => d.hostname === 'api.example.com')!;
    assert.equal(https.scheme, 'https');
    assert.equal(https.port, undefined);
  });

  // -----------------------------------------------------------------------
  // 2. Bare-hostname extraction from API calls
  // -----------------------------------------------------------------------
  it('extracts bare hostnames from fetch, axios, http.get, and new URL calls', () => {
    const files: DiscoveredFile[] = [
      file('src/requests.ts', [
        'fetch("api.internal.io/health");',
        'axios("metrics.corp.net:9090/query");',
        'http.get("telemetry.service.com/report");',
        'new URL("registry.npmjs.org/package");',
      ]),
    ];

    const domains = extractDomains(files);
    const hostnames = domains.map(d => d.hostname);

    assert.ok(hostnames.includes('api.internal.io'), 'fetch bare hostname');
    assert.ok(hostnames.includes('metrics.corp.net'), 'axios bare hostname');
    assert.ok(hostnames.includes('telemetry.service.com'), 'http.get bare hostname');
    assert.ok(hostnames.includes('registry.npmjs.org'), 'new URL bare hostname');

    const metrics = domains.find(d => d.hostname === 'metrics.corp.net')!;
    assert.equal(metrics.port, 9090);
    assert.equal(metrics.scheme, 'https', 'bare domains default to https');
  });

  // -----------------------------------------------------------------------
  // 3. Deduplication by hostname+port
  // -----------------------------------------------------------------------
  it('deduplicates domains by hostname+port, keeping first occurrence', () => {
    const files: DiscoveredFile[] = [
      file('src/a.ts', [
        'fetch("https://api.example.com/v1");',
      ]),
      file('src/b.ts', [
        'fetch("https://api.example.com/v2");',
        'fetch("https://api.example.com:3000/v1");',
      ]),
    ];

    const domains = extractDomains(files);

    // api.example.com (no port) should appear once — from first file
    const noPort = domains.filter(d => d.hostname === 'api.example.com' && d.port === undefined);
    assert.equal(noPort.length, 1, 'should deduplicate same hostname without port');
    assert.equal(noPort[0]!.sourceFile, 'src/a.ts', 'should keep first occurrence');

    // api.example.com:3000 is a different key, should also appear
    const withPort = domains.filter(d => d.hostname === 'api.example.com' && d.port === 3000);
    assert.equal(withPort.length, 1, 'hostname with different port is a separate entry');
  });

  // -----------------------------------------------------------------------
  // 4. Localhost filtering with non-standard port edge case
  // -----------------------------------------------------------------------
  it('excludes localhost with standard ports but includes with non-standard ports', () => {
    const files: DiscoveredFile[] = [
      file('src/dev.ts', [
        'const a = "http://localhost/api";',
        'const b = "http://127.0.0.1:80/health";',
        'const c = "https://localhost:443/secure";',
        'const d = "http://localhost:3000/dev";',
        'const e = "http://127.0.0.1:8080/debug";',
      ]),
    ];

    const domains = extractDomains(files);
    const hostnames = domains.map(d => `${d.hostname}:${d.port ?? 'default'}`);

    // Standard ports excluded
    assert.ok(!hostnames.includes('localhost:default'), 'localhost without port excluded');
    assert.ok(!hostnames.includes('127.0.0.1:80'), 'localhost:80 excluded');
    assert.ok(!hostnames.includes('localhost:443'), 'localhost:443 excluded');

    // Non-standard ports included
    assert.ok(hostnames.includes('localhost:3000'), 'localhost:3000 included');
    assert.ok(hostnames.includes('127.0.0.1:8080'), '127.0.0.1:8080 included');
  });

  // -----------------------------------------------------------------------
  // 5. file:// URI and unix socket path exclusion
  // -----------------------------------------------------------------------
  it('does not extract file:// URIs or unix socket paths as domains', () => {
    const files: DiscoveredFile[] = [
      file('src/files.ts', [
        'const db = "file:///var/data/app.db";',
        'const sock = "/var/run/docker.sock";',
        'const abs = "/usr/local/bin/node";',
        'const rel = "./config/settings.json";',
        'const real = "https://real.example.com/api";',
      ]),
    ];

    const domains = extractDomains(files);

    assert.equal(domains.length, 1, 'only the real https URL should be extracted');
    assert.equal(domains[0]!.hostname, 'real.example.com');

    // Verify no file paths leaked through
    for (const d of domains) {
      assert.ok(!d.hostname.includes('/'), 'hostname should not contain path separators');
      assert.notEqual(d.scheme, 'file', 'file scheme must not appear');
    }
  });

  // -----------------------------------------------------------------------
  // 6. Multi-format config file scanning (.ts, .js, .json, .yaml, .yml, .env)
  // -----------------------------------------------------------------------
  it('scans .ts, .js, .json, .yaml, .yml, and .env files for domains', () => {
    const files: DiscoveredFile[] = [
      file('src/app.ts', [
        'const API = "https://ts.example.com/api";',
      ]),
      file('lib/config.js', [
        'module.exports = { url: "https://js.example.com/config" };',
      ]),
      file('config/endpoints.json', [
        '{',
        '  "api": "https://json.example.com/v2",',
        '  "ws": "wss://json-ws.example.com:9000/stream"',
        '}',
      ]),
      file('deploy/config.yaml', [
        'api_url: https://yaml.example.com/api',
      ]),
      file('deploy/secrets.yml', [
        'webhook: https://yml.example.com/hooks',
      ]),
      file('.env', [
        'API_HOST=https://env.example.com/v1',
      ]),
      // This extension should NOT be scanned
      file('README.md', [
        'Visit https://readme.example.com for docs.',
      ]),
    ];

    const domains = extractDomains(files);
    const hostnames = domains.map(d => d.hostname);

    assert.ok(hostnames.includes('ts.example.com'), '.ts scanned');
    assert.ok(hostnames.includes('js.example.com'), '.js scanned');
    assert.ok(hostnames.includes('json.example.com'), '.json scanned');
    assert.ok(hostnames.includes('json-ws.example.com'), '.json wss scanned');
    assert.ok(hostnames.includes('yaml.example.com'), '.yaml scanned');
    assert.ok(hostnames.includes('yml.example.com'), '.yml scanned');
    assert.ok(hostnames.includes('env.example.com'), '.env scanned');
    assert.ok(!hostnames.includes('readme.example.com'), '.md should NOT be scanned');

    // Verify all Domain fields are populated
    for (const d of domains) {
      assert.ok(typeof d.hostname === 'string' && d.hostname.length > 0);
      assert.ok(typeof d.scheme === 'string' && d.scheme.length > 0);
      assert.ok(typeof d.sourceFile === 'string' && d.sourceFile.length > 0);
      assert.ok(typeof d.line === 'number' && d.line >= 1);
      assert.ok(typeof d.context === 'string' && d.context.length > 0);
    }
  });
});
