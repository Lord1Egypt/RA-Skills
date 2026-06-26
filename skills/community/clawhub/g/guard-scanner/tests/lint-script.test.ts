import { describe, it, expect, assert, beforeEach, afterEach, vi, test } from 'vitest';
// import test from 'node:test'; // Removed incompatible node:test import

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import { collectLintTargets, lintFiles } from '../scripts/lint.ts';

test('collectLintTargets collects TypeScript files', () => {
  const targets = collectLintTargets(path.join(process.cwd(), 'scripts'));
  assert.ok(targets.some((p) => p.endsWith('scripts/lint.ts')));
});

test('lintFiles accepts valid TypeScript', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'guard-lint-ok-'));
  const file = path.join(dir, 'ok.ts');
  fs.writeFileSync(file, 'const a: number = 1;\n');

  assert.doesNotThrow(() => lintFiles([file]));
});

test('lintFiles rejects invalid TypeScript syntax', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'guard-lint-ng-'));
  const file = path.join(dir, 'bad.ts');
  fs.writeFileSync(file, 'const broken: number = ;\n');

  assert.throws(() => lintFiles([file]), /Syntax lint failed/);
});
