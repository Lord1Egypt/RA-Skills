import { describe, it } from 'node:test';
import assert from 'node:assert/strict';
import { extractFilePaths } from '../src/extract.js';
import type { DiscoveredFile } from '../src/types.js';

/** Creates a DiscoveredFile from an inline source string. */
function createSource(content: string, path = 'src/app.ts'): DiscoveredFile {
  return { path, content };
}

describe('extractFilePaths – file access detection', () => {
  // ── 1. fs.readFileSync and fs.readFile (read APIs) ────────────────────
  it('detects readFileSync and readFile as read-access paths', () => {
    const source = createSource([
      "import fs from 'fs';",
      "const data = fs.readFileSync('/etc/hosts', 'utf-8');",
      "fs.readFile('/var/log/app.log', 'utf-8', cb);",
    ].join('\n'));

    const paths = extractFilePaths([source]);

    const hosts = paths.find(p => p.path === '/etc/hosts');
    assert.ok(hosts, '/etc/hosts should be detected');
    assert.equal(hosts.accessType, 'read');
    assert.equal(hosts.line, 2);

    const log = paths.find(p => p.path === '/var/log/app.log');
    assert.ok(log, '/var/log/app.log should be detected');
    assert.equal(log.accessType, 'read');
    assert.equal(log.line, 3);
  });

  // ── 2. fs.writeFileSync, appendFile, createWriteStream (write APIs) ───
  it('detects writeFileSync, appendFile, and createWriteStream as write-access', () => {
    const source = createSource([
      "fs.writeFileSync('/tmp/output.json', data);",
      "fs.appendFile('/var/log/audit.log', entry, cb);",
      "const ws = fs.createWriteStream('/tmp/stream.bin');",
    ].join('\n'));

    const paths = extractFilePaths([source]);

    const output = paths.find(p => p.path === '/tmp/output.json');
    assert.ok(output, '/tmp/output.json should be detected');
    assert.equal(output.accessType, 'write');

    const audit = paths.find(p => p.path === '/var/log/audit.log');
    assert.ok(audit, '/var/log/audit.log should be detected');
    assert.equal(audit.accessType, 'write');

    const stream = paths.find(p => p.path === '/tmp/stream.bin');
    assert.ok(stream, '/tmp/stream.bin should be detected');
    assert.equal(stream.accessType, 'write');
  });

  // ── 3. path.join with dynamic variable segment ────────────────────────
  it('detects absolute path literals inside path.join with dynamic segments', () => {
    const source = createSource([
      "const configPath = path.join(baseDir, '/config/app.yaml');",
      "const dataPath = path.join(process.cwd(), '/data/seed.json');",
    ].join('\n'));

    const paths = extractFilePaths([source]);

    const config = paths.find(p => p.path === '/config/app.yaml');
    assert.ok(config, '/config/app.yaml should be detected from path.join');
    assert.equal(config.accessType, 'unknown');

    const seed = paths.find(p => p.path === '/data/seed.json');
    assert.ok(seed, '/data/seed.json should be detected from path.join');
    assert.equal(seed.accessType, 'unknown');
  });

  // ── 4. Simple wildcard glob (*.json) ──────────────────────────────────
  it('detects simple * wildcard glob in an fs read call', () => {
    const source = createSource([
      "const configs = readFileSync('/etc/app/*.json', 'utf-8');",
    ].join('\n'));

    const paths = extractFilePaths([source]);

    const glob = paths.find(p => p.path === '/etc/app/*.json');
    assert.ok(glob, '/etc/app/*.json glob should be detected');
    assert.equal(glob.accessType, 'read');
    assert.equal(glob.line, 1);
    assert.ok(glob.path.includes('*'), 'path preserves wildcard character');
  });

  // ── 5. Recursive glob (**/*.ts) ───────────────────────────────────────
  it('detects recursive ** glob in an absolute path literal', () => {
    const source = createSource([
      "const tsFiles = '/project/src/**/*.ts';",
      "const matches = glob.sync(tsFiles);",
    ].join('\n'));

    const paths = extractFilePaths([source]);

    const recursive = paths.find(p => p.path === '/project/src/**/*.ts');
    assert.ok(recursive, '/project/src/**/*.ts should be detected');
    assert.equal(recursive.accessType, 'unknown');
    assert.ok(recursive.path.includes('**'), 'path preserves ** recursive glob');
  });

  // ── 6. Glob combined with path.join ───────────────────────────────────
  it('detects absolute segments from path.join but not bare glob literals', () => {
    const source = createSource([
      "const logDir = path.join('/var/log', appName);",
      "const pattern = path.join(logDir, '**/*.log');",
      "const allTmp = glob.sync('/tmp/cache/**/*.tmp');",
    ].join('\n'));

    const paths = extractFilePaths([source]);

    // Absolute prefix from path.join is detected
    const varLog = paths.find(p => p.path === '/var/log');
    assert.ok(varLog, '/var/log should be extracted from path.join');
    assert.equal(varLog.accessType, 'unknown');

    // Full absolute glob path is detected
    const tmpGlob = paths.find(p => p.path === '/tmp/cache/**/*.tmp');
    assert.ok(tmpGlob, '/tmp/cache/**/*.tmp should be detected');
    assert.ok(tmpGlob.path.includes('**'), 'preserves ** in glob path');

    // Bare glob segment without a path prefix is not detected
    const bareGlob = paths.find(p => p.path === '**/*.log');
    assert.equal(bareGlob, undefined, 'bare **/*.log lacks path prefix and should not be detected');
  });
});
