import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { test } from 'node:test';

const packageRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const manifest = JSON.parse(fs.readFileSync(path.join(packageRoot, 'package.json'), 'utf8'));

test('package publishes an installable public CLI artifact', () => {
  assert.equal(manifest.bin['klik-import'], 'dist/klik-import.mjs');
  assert.equal(manifest.publishConfig.access, 'public');
  assert.ok(manifest.files.includes('dist'));
  assert.ok(manifest.files.includes('SKILL.md'));
  assert.match(manifest.repository.url, /github\.com\/minervacap2022\/klik-import-skill/);
});

test('CLI finds SKILL.md when invoked through a package bin symlink', () => {
  const temporaryDirectory = fs.mkdtempSync(path.join(os.tmpdir(), 'klik-import-test-'));
  try {
    const binDirectory = path.join(temporaryDirectory, 'node_modules', '.bin');
    const cliPath = path.join(binDirectory, 'klik-import');
    fs.mkdirSync(binDirectory, { recursive: true });
    fs.symlinkSync(path.join(packageRoot, 'dist', 'klik-import.mjs'), cliPath);

    const result = spawnSync(process.execPath, [cliPath, 'doctor'], { encoding: 'utf8' });
    assert.equal(result.status, 0, result.stderr);
    assert.match(result.stdout, /SKILL\.md present: ok/);
  } finally {
    fs.rmSync(temporaryDirectory, { recursive: true, force: true });
  }
});
