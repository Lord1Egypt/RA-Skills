import { describe, it, beforeEach, afterEach } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { discoverFiles, loadIgnorePatterns, shouldIgnoreEntry, parseSkillFrontmatter, parsePackageJson, readSkillMetadata } from '../src/discovery.js';

function makeTmpDir(): string {
  return fs.mkdtempSync(path.join(os.tmpdir(), 'discovery-test-'));
}

function writeFile(base: string, relPath: string, content = ''): void {
  const full = path.join(base, relPath);
  fs.mkdirSync(path.dirname(full), { recursive: true });
  fs.writeFileSync(full, content);
}

describe('discoverFiles', () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = makeTmpDir();
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('returns correct relative POSIX paths for nested files', async () => {
    writeFile(tmpDir, 'src/index.ts', 'export {}');
    writeFile(tmpDir, 'src/utils/helpers.ts', 'export {}');
    writeFile(tmpDir, 'README.md', '# hello');

    const files = await discoverFiles(tmpDir);

    assert.deepEqual(files, [
      'README.md',
      'src/index.ts',
      'src/utils/helpers.ts',
    ]);
  });

  it('excludes node_modules directory', async () => {
    writeFile(tmpDir, 'src/index.ts', 'export {}');
    writeFile(tmpDir, 'node_modules/pkg/index.js', 'module.exports = {}');

    const files = await discoverFiles(tmpDir);

    assert.deepEqual(files, ['src/index.ts']);
    assert.ok(!files.some(f => f.includes('node_modules')));
  });

  it('excludes directories listed in .skillignore', async () => {
    writeFile(tmpDir, 'src/index.ts', 'export {}');
    writeFile(tmpDir, 'vendor/lib.js', 'module.exports = {}');
    writeFile(tmpDir, 'tmp/cache.bin', '');
    fs.writeFileSync(
      path.join(tmpDir, '.skillignore'),
      '# custom ignores\nvendor\n\ntmp\n',
    );

    const files = await discoverFiles(tmpDir);

    assert.deepEqual(files, ['.skillignore', 'src/index.ts']);
    assert.ok(!files.some(f => f.includes('vendor')));
    assert.ok(!files.some(f => f.includes('tmp')));
  });

  it('skips symlinks', async () => {
    writeFile(tmpDir, 'real.ts', 'export {}');
    fs.symlinkSync(
      path.join(tmpDir, 'real.ts'),
      path.join(tmpDir, 'link.ts'),
    );

    const files = await discoverFiles(tmpDir);

    assert.deepEqual(files, ['real.ts']);
    assert.ok(!files.includes('link.ts'));
  });

  it('returns empty array for empty directory', async () => {
    const files = await discoverFiles(tmpDir);
    assert.deepEqual(files, []);
  });
});

describe('shouldIgnoreEntry', () => {
  it('returns true when entryName matches an ignore pattern', () => {
    assert.equal(shouldIgnoreEntry('node_modules', ['node_modules', '.git'], false), true);
    assert.equal(shouldIgnoreEntry('.git', ['node_modules', '.git'], false), true);
  });

  it('returns false when entryName does not match any pattern', () => {
    assert.equal(shouldIgnoreEntry('src', ['node_modules', '.git'], false), false);
    assert.equal(shouldIgnoreEntry('index.ts', ['node_modules', '.git'], false), false);
  });

  it('returns true when entry is a symlink regardless of pattern match', () => {
    assert.equal(shouldIgnoreEntry('src', [], true), true);
    assert.equal(shouldIgnoreEntry('anything', ['node_modules'], true), true);
  });

  it('uses case-sensitive matching', () => {
    assert.equal(shouldIgnoreEntry('Node_Modules', ['node_modules'], false), false);
    assert.equal(shouldIgnoreEntry('NODE_MODULES', ['node_modules'], false), false);
  });

  it('returns false for empty ignore list and non-symlink', () => {
    assert.equal(shouldIgnoreEntry('file.ts', [], false), false);
  });
});

describe('loadIgnorePatterns', () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = makeTmpDir();
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('returns hardcoded list when no .skillignore exists', () => {
    const patterns = loadIgnorePatterns(tmpDir);
    assert.deepEqual(patterns, [
      'node_modules',
      '.git',
      'dist',
      'coverage',
      '.saturnday',
    ]);
  });

  it('merges .skillignore patterns with hardcoded list', () => {
    fs.writeFileSync(
      path.join(tmpDir, '.skillignore'),
      '# comment\nvendor\n\ntmp\n',
    );
    const patterns = loadIgnorePatterns(tmpDir);
    assert.deepEqual(patterns, [
      'node_modules',
      '.git',
      'dist',
      'coverage',
      '.saturnday',
      'vendor',
      'tmp',
    ]);
  });

  it('does not duplicate patterns already in hardcoded list', () => {
    fs.writeFileSync(
      path.join(tmpDir, '.skillignore'),
      'node_modules\ncustom\n',
    );
    const patterns = loadIgnorePatterns(tmpDir);
    const nodeModulesCount = patterns.filter(p => p === 'node_modules').length;
    assert.equal(nodeModulesCount, 1);
    assert.ok(patterns.includes('custom'));
  });
});

describe('parseSkillFrontmatter', () => {
  it('parses valid frontmatter into partial SkillMetadata', () => {
    const content = [
      '---',
      'name: my-skill',
      'version: 1.2.3',
      'permissions:',
      '  - network',
      '  - fs-read',
      '---',
      '# My Skill',
      'Some description.',
    ].join('\n');

    const result = parseSkillFrontmatter(content);
    assert.equal(result.name, 'my-skill');
    assert.equal(result.version, '1.2.3');
    assert.deepEqual(result.declaredPermissions, ['network', 'fs-read']);
  });

  it('returns empty object when no delimiters are present', () => {
    const result = parseSkillFrontmatter('# Just markdown\nNo frontmatter here.');
    assert.deepEqual(result, {});
  });

  it('returns empty object for malformed YAML without throwing', () => {
    const content = [
      '---',
      'name: [invalid',
      '  yaml: {{broken',
      '---',
    ].join('\n');

    const result = parseSkillFrontmatter(content);
    assert.deepEqual(result, {});
  });

  it('returns empty object for empty frontmatter block', () => {
    const content = '---\n---\nBody content.';
    const result = parseSkillFrontmatter(content);
    assert.deepEqual(result, {});
  });

  it('extracts only recognized fields and ignores extras', () => {
    const content = [
      '---',
      'name: cool-skill',
      'author: someone',
      'version: 0.0.1',
      '---',
    ].join('\n');

    const result = parseSkillFrontmatter(content);
    assert.equal(result.name, 'cool-skill');
    assert.equal(result.version, '0.0.1');
    assert.equal(result.declaredPermissions, undefined);
    assert.equal((result as Record<string, unknown>).author, undefined);
  });
});

describe('parsePackageJson', () => {
  it('extracts dependencies and devDependencies into declaredDependencies', () => {
    const content = JSON.stringify({
      name: 'my-pkg',
      dependencies: { axios: '^1.0.0', lodash: '^4.17.0' },
      devDependencies: { vitest: '^1.0.0' },
    });

    const result = parsePackageJson(content);
    assert.deepEqual(result.declaredDependencies, {
      axios: '^1.0.0',
      lodash: '^4.17.0',
      vitest: '^1.0.0',
    });
  });

  it('extracts openclaw permissions into declaredPermissions', () => {
    const content = JSON.stringify({
      name: 'oc-pkg',
      dependencies: { got: '^12.0.0' },
      openclaw: { permissions: ['network', 'shell'] },
    });

    const result = parsePackageJson(content);
    assert.deepEqual(result.declaredPermissions, ['network', 'shell']);
    assert.deepEqual(result.declaredDependencies, { got: '^12.0.0' });
  });

  it('returns empty object on malformed JSON without throwing', () => {
    const result = parsePackageJson('{ not valid json !!!');
    assert.deepEqual(result, {});
  });

  it('returns empty dependencies when neither dependencies nor devDependencies exist', () => {
    const content = JSON.stringify({ name: 'bare-pkg', version: '1.0.0' });

    const result = parsePackageJson(content);
    assert.deepEqual(result.declaredDependencies, {});
    assert.equal(result.declaredPermissions, undefined);
  });

  it('filters out non-string values from openclaw permissions', () => {
    const content = JSON.stringify({
      name: 'mixed-pkg',
      openclaw: { permissions: ['network', 42, null, 'fs-read', true] },
    });

    const result = parsePackageJson(content);
    assert.deepEqual(result.declaredPermissions, ['network', 'fs-read']);
  });

  it('returns empty object for non-object JSON values', () => {
    assert.deepEqual(parsePackageJson('"just a string"'), {});
    assert.deepEqual(parsePackageJson('42'), {});
    assert.deepEqual(parsePackageJson('null'), {});
    assert.deepEqual(parsePackageJson('[1,2,3]'), {});
  });

  it('devDependencies override dependencies when keys collide', () => {
    const content = JSON.stringify({
      dependencies: { pkg: '^1.0.0' },
      devDependencies: { pkg: '^2.0.0' },
    });

    const result = parsePackageJson(content);
    assert.equal(result.declaredDependencies!.pkg, '^2.0.0');
  });
});

describe('readSkillMetadata', () => {
  let tmpDir: string;

  beforeEach(() => {
    tmpDir = makeTmpDir();
  });

  afterEach(() => {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  });

  it('returns full metadata from valid SKILL.md and package.json', async () => {
    writeFile(tmpDir, 'SKILL.md', [
      '---',
      'name: test-skill',
      'version: 2.0.0',
      'permissions:',
      '  - network',
      '---',
      '# Test Skill',
    ].join('\n'));

    writeFile(tmpDir, 'package.json', JSON.stringify({
      name: 'test-skill',
      dependencies: { axios: '^1.0.0', lodash: '^4.17.0' },
    }));

    const meta = await readSkillMetadata(tmpDir);
    assert.equal(meta.name, 'test-skill');
    assert.equal(meta.version, '2.0.0');
    assert.deepEqual(meta.declaredPermissions, ['network']);
    assert.deepEqual(meta.declaredDependencies, { axios: '^1.0.0', lodash: '^4.17.0' });
  });

  it('returns defaults when SKILL.md is missing', async () => {
    writeFile(tmpDir, 'package.json', JSON.stringify({
      name: 'pkg-only',
      dependencies: { express: '^4.0.0' },
    }));

    const meta = await readSkillMetadata(tmpDir);
    assert.equal(meta.name, 'unknown');
    assert.equal(meta.version, 'unknown');
    assert.deepEqual(meta.declaredPermissions, []);
    assert.deepEqual(meta.declaredDependencies, { express: '^4.0.0' });
  });

  it('returns SKILL.md data with empty dependencies when package.json is missing', async () => {
    writeFile(tmpDir, 'SKILL.md', [
      '---',
      'name: solo-skill',
      'version: 0.1.0',
      'permissions:',
      '  - fs-read',
      '---',
    ].join('\n'));

    const meta = await readSkillMetadata(tmpDir);
    assert.equal(meta.name, 'solo-skill');
    assert.equal(meta.version, '0.1.0');
    assert.deepEqual(meta.declaredPermissions, ['fs-read']);
    assert.deepEqual(meta.declaredDependencies, {});
  });

  it('returns defaults without throwing on malformed YAML frontmatter', async () => {
    writeFile(tmpDir, 'SKILL.md', [
      '---',
      'name: [invalid',
      '  yaml: {{broken',
      '---',
    ].join('\n'));

    const meta = await readSkillMetadata(tmpDir);
    assert.equal(meta.name, 'unknown');
    assert.equal(meta.version, 'unknown');
    assert.deepEqual(meta.declaredPermissions, []);
  });

  it('extracts openclaw permissions from package.json', async () => {
    writeFile(tmpDir, 'SKILL.md', [
      '---',
      'name: oc-skill',
      'version: 1.0.0',
      'permissions:',
      '  - network',
      '---',
    ].join('\n'));

    writeFile(tmpDir, 'package.json', JSON.stringify({
      name: 'oc-skill',
      dependencies: { got: '^12.0.0' },
      openclaw: { permissions: ['shell', 'env'] },
    }));

    const meta = await readSkillMetadata(tmpDir);
    assert.equal(meta.name, 'oc-skill');
    assert.deepEqual(meta.declaredPermissions, ['network', 'shell', 'env']);
    assert.deepEqual(meta.declaredDependencies, { got: '^12.0.0' });
  });
});
