import { describe, it, before, after } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { analyzeSkill, extractPerFile } from '../src/index.js';
import type { DiagnosticWarning, DiscoveredFile } from '../src/index.js';

describe('analyzeSkill', () => {
  let tmpDir: string;

  before(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'pmg-test-'));
  });

  after(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('returns diagnostic for non-existent directory', async () => {
    const result = await analyzeSkill(path.join(tmpDir, 'does-not-exist'));
    assert.equal(result.markdownManifest, '');
    assert.deepEqual(result.jsonManifest, {});
    assert.ok(result.diagnostics.length > 0);
    assert.equal(result.diagnostics[0]!.stage, 'discovery');
    assert.ok(result.diagnostics[0]!.message.includes('No files discovered'));
  });

  it('returns diagnostic for empty directory', async () => {
    const dir = path.join(tmpDir, 'empty');
    fs.mkdirSync(dir);
    const result = await analyzeSkill(dir);
    assert.equal(result.markdownManifest, '');
    assert.deepEqual(result.jsonManifest, {});
    assert.ok(result.diagnostics.some(d => d.message.includes('No files discovered')));
  });

  it('produces both manifests for a valid skill directory', async () => {
    const dir = path.join(tmpDir, 'valid');
    fs.mkdirSync(dir);
    fs.writeFileSync(path.join(dir, 'main.ts'), 'const x = 1;\n');
    const result = await analyzeSkill(dir);
    assert.ok(result.markdownManifest.length > 0, 'markdown manifest should not be empty');
    assert.ok(typeof result.jsonManifest === 'object' && result.jsonManifest !== null);
    assert.ok(Array.isArray(result.diagnostics));
  });

  it('detects network domains in skill files', async () => {
    const dir = path.join(tmpDir, 'net');
    fs.mkdirSync(dir);
    fs.writeFileSync(path.join(dir, 'api.ts'), 'fetch("https://api.example.com/data");\n');
    const result = await analyzeSkill(dir);
    const json = result.jsonManifest as Record<string, unknown>;
    const observed = json['observed'] as Record<string, string[]>;
    assert.ok(observed['network'].includes('api.example.com'));
  });

  it('detects environment variables', async () => {
    const dir = path.join(tmpDir, 'env');
    fs.mkdirSync(dir);
    fs.writeFileSync(path.join(dir, 'config.ts'), 'const key = process.env.API_KEY;\n');
    const result = await analyzeSkill(dir);
    const json = result.jsonManifest as Record<string, unknown>;
    const observed = json['observed'] as Record<string, string[]>;
    assert.ok(observed['envVars'].includes('API_KEY'));
  });

  it('does not throw when pipeline stages encounter errors', async () => {
    const dir = path.join(tmpDir, 'robust');
    fs.mkdirSync(dir);
    fs.writeFileSync(path.join(dir, 'ok.ts'), 'console.log("hello");\n');
    const result = await analyzeSkill(dir);
    assert.ok(typeof result.markdownManifest === 'string');
    assert.ok(typeof result.jsonManifest === 'object');
  });

  it('markdownManifest contains skill name heading', async () => {
    const dir = path.join(tmpDir, 'named');
    fs.mkdirSync(dir);
    fs.writeFileSync(
      path.join(dir, 'SKILL.md'),
      '---\nname: test-skill\nversion: 1.0.0\n---\nA test skill.\n',
    );
    fs.writeFileSync(path.join(dir, 'run.ts'), 'const a = 1;\n');
    const result = await analyzeSkill(dir);
    assert.ok(result.markdownManifest.includes('test-skill'));
  });

  it('jsonManifest contains expected top-level keys', async () => {
    const dir = path.join(tmpDir, 'keys');
    fs.mkdirSync(dir);
    fs.writeFileSync(path.join(dir, 'index.ts'), 'export {};\n');
    const result = await analyzeSkill(dir);
    const json = result.jsonManifest as Record<string, unknown>;
    assert.ok('skill_name' in json);
    assert.ok('disposition' in json);
    assert.ok('observed' in json);
    assert.ok('mismatches' in json);
    assert.ok('summary' in json);
  });

  it('captures read failures in diagnostics without throwing', async () => {
    const dir = path.join(tmpDir, 'mixed');
    fs.mkdirSync(dir);
    fs.writeFileSync(path.join(dir, 'good.ts'), 'const x = 1;\n');
    const binPath = path.join(dir, 'data.bin');
    fs.writeFileSync(binPath, Buffer.from([0x80, 0x81, 0x82, 0x00, 0xff]));
    const result = await analyzeSkill(dir);
    assert.ok(result.markdownManifest.length > 0);
  });

  it('all files succeed → diagnostics array has no extraction errors', async () => {
    const dir = path.join(tmpDir, 'all-ok');
    fs.mkdirSync(dir);
    fs.writeFileSync(path.join(dir, 'a.ts'), 'const x = 1;\n');
    fs.writeFileSync(path.join(dir, 'b.ts'), 'const y = 2;\n');
    const result = await analyzeSkill(dir);
    const extractionDiags = result.diagnostics.filter(d => d.stage === 'extraction');
    assert.equal(extractionDiags.length, 0);
  });

  it('one file throws during extraction → partial results and diagnostic present', async () => {
    const diags: DiagnosticWarning[] = [];
    const goodFile = { path: 'good.ts', content: 'fetch("https://example.com/api");\n' };
    const badFile: { path: string; content: string } = { path: 'bad.ts', content: '' };
    Object.defineProperty(badFile, 'content', {
      get() { throw new Error('simulated extraction failure'); },
      configurable: true,
    });

    const result = await extractPerFile([goodFile, badFile], [], '/tmp', diags);

    // Good file's domain extraction should succeed
    assert.ok(result.network.includes('example.com'), 'partial results should include good file data');
    // Bad file should produce exactly one extraction diagnostic
    assert.equal(diags.length, 1);
    assert.equal(diags[0]!.file, 'bad.ts');
    assert.equal(diags[0]!.stage, 'extraction');
    assert.ok(diags[0]!.error.includes('simulated extraction failure'));
  });
});

// ---------------------------------------------------------------------------
// extractPerFile deduplication tests — weighted by category risk
// ---------------------------------------------------------------------------

describe('extractPerFile dedup', () => {
  let tmpDir: string;

  before(() => {
    tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'pmg-dedup-'));
  });

  after(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  // --- shellCommands (weight 8): 3 tests ---

  it('deduplicates identical exec commands across files', async () => {
    const files: DiscoveredFile[] = [
      { path: 'a.ts', content: 'exec("ls -la");\n' },
      { path: 'b.ts', content: 'exec("ls -la");\n' },
    ];
    const diags: DiagnosticWarning[] = [];
    const result = await extractPerFile(files, [], tmpDir, diags);
    assert.equal(result.shellCommands.length, 1);
    assert.ok(result.shellCommands.includes('ls -la'));
  });

  it('deduplicates spawn commands referencing the same binary across files', async () => {
    const files: DiscoveredFile[] = [
      { path: 'x.ts', content: 'spawn("node");\nspawn("git");\n' },
      { path: 'y.ts', content: 'spawn("node");\n' },
    ];
    const diags: DiagnosticWarning[] = [];
    const result = await extractPerFile(files, [], tmpDir, diags);
    assert.equal(result.shellCommands.length, 2);
    assert.ok(result.shellCommands.includes('node'));
    assert.ok(result.shellCommands.includes('git'));
  });

  it('deduplicates same command from backtick and $() subshell patterns', async () => {
    const files: DiscoveredFile[] = [
      { path: 'a.sh', content: 'echo `whoami`\n' },
      { path: 'b.sh', content: 'echo $(whoami)\n' },
    ];
    const diags: DiagnosticWarning[] = [];
    const result = await extractPerFile(files, [], tmpDir, diags);
    assert.equal(result.shellCommands.length, 1);
    assert.ok(result.shellCommands.includes('whoami'));
  });

  // --- binaries (weight 5): 2 tests ---

  it('deduplicates same binary discovered via CLI patterns in multiple files', async () => {
    const dir = path.join(tmpDir, 'bin-multi');
    fs.mkdirSync(dir);
    fs.writeFileSync(path.join(dir, 'a.ts'), 'const cmd = "git status";\n');
    fs.writeFileSync(path.join(dir, 'b.ts'), 'const cmd = "git pull";\n');
    const diags: DiagnosticWarning[] = [];
    const result = await extractPerFile([], ['a.ts', 'b.ts'], dir, diags);
    assert.equal(result.binaries.length, 1);
    assert.ok(result.binaries.includes('git'));
  });

  it('deduplicates binary found in both shebang and inline string', async () => {
    const dir = path.join(tmpDir, 'bin-shebang');
    fs.mkdirSync(dir);
    // Shebang produces "node", known-CLI scan also finds "node" from the string literal
    fs.writeFileSync(path.join(dir, 'run.sh'), '#!/usr/bin/env node\nCMD="node build"\n');
    const diags: DiagnosticWarning[] = [];
    const result = await extractPerFile([], ['run.sh'], dir, diags);
    assert.equal(result.binaries.length, 1);
    assert.ok(result.binaries.includes('node'));
  });

  // --- network (weight 6): 1 test ---

  it('deduplicates same domain from fetch calls across files', async () => {
    const files: DiscoveredFile[] = [
      { path: 'api.ts', content: 'fetch("https://api.example.com/users");\n' },
      { path: 'client.ts', content: 'fetch("https://api.example.com/posts");\n' },
    ];
    const diags: DiagnosticWarning[] = [];
    const result = await extractPerFile(files, [], tmpDir, diags);
    assert.equal(result.network.length, 1);
    assert.ok(result.network.includes('api.example.com'));
  });

  // --- envVars (weight 4): 1 test ---

  it('deduplicates same env var read in two files', async () => {
    const files: DiscoveredFile[] = [
      { path: 'config.ts', content: 'const url = process.env.DATABASE_URL;\n' },
      { path: 'db.ts', content: 'const conn = process.env.DATABASE_URL;\n' },
    ];
    const diags: DiagnosticWarning[] = [];
    const result = await extractPerFile(files, [], tmpDir, diags);
    assert.equal(result.envVars.length, 1);
    assert.ok(result.envVars.includes('DATABASE_URL'));
  });

  // --- filePaths + configFiles + packageManagers (weight 2-3): 1 test ---

  it('deduplicates filePaths, configFiles, and packageManagers simultaneously', async () => {
    const files: DiscoveredFile[] = [
      { path: 'a.ts', content: 'readFileSync("/etc/hosts");\nconst c = ".eslintrc";\nconst s = "pip install requests";\n' },
      { path: 'b.ts', content: 'readFileSync("/etc/hosts");\nconst c = ".eslintrc";\nconst s = "pip install requests";\n' },
    ];
    const diags: DiagnosticWarning[] = [];
    const result = await extractPerFile(files, [], tmpDir, diags);
    assert.equal(result.filePaths.length, 1);
    assert.ok(result.filePaths.includes('/etc/hosts'));
    assert.equal(result.configFiles.length, 1);
    assert.ok(result.configFiles.includes('.eslintrc'));
    assert.equal(result.packageManagers.length, 1);
    assert.ok(result.packageManagers.includes('pip'));
  });

  // --- Cross-category: 1 test ---

  it('deduplicates across all categories simultaneously', async () => {
    const dir = path.join(tmpDir, 'cross-cat');
    fs.mkdirSync(dir);
    const content = [
      'exec("npm install");',
      'fetch("https://api.example.com/data");',
      'const key = process.env.SECRET_KEY;',
      'readFileSync("/etc/passwd");',
      'const cfg = ".npmrc";',
    ].join('\n') + '\n';

    // On-disk files for binary extraction (exec("npm install") → binary "npm")
    fs.writeFileSync(path.join(dir, 'one.ts'), content);
    fs.writeFileSync(path.join(dir, 'two.ts'), content);

    // Matching in-memory files for all other categories
    const files: DiscoveredFile[] = [
      { path: 'one.ts', content },
      { path: 'two.ts', content },
    ];
    const diags: DiagnosticWarning[] = [];
    const result = await extractPerFile(files, ['one.ts', 'two.ts'], dir, diags);

    assert.equal(result.binaries.length, 1);
    assert.ok(result.binaries.includes('npm'));
    assert.equal(result.shellCommands.length, 1);
    assert.ok(result.shellCommands.includes('npm install'));
    assert.equal(result.network.length, 1);
    assert.ok(result.network.includes('api.example.com'));
    assert.equal(result.envVars.length, 1);
    assert.ok(result.envVars.includes('SECRET_KEY'));
    assert.equal(result.filePaths.length, 1);
    assert.ok(result.filePaths.includes('/etc/passwd'));
    assert.equal(result.configFiles.length, 1);
    assert.ok(result.configFiles.includes('.npmrc'));
    assert.equal(result.packageManagers.length, 1);
    assert.ok(result.packageManagers.includes('npm'));
  });
});
