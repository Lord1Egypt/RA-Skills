import test from 'node:test';
import assert from 'node:assert/strict';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const skillRoot = path.resolve(__dirname, '..');

test('validate-state CLI succeeds against example state', () => {
  // SECURITY: Safe test-only shell execution
  // This test executes the project's own CLI validation tool with fixed,
  // static arguments (no user input). This is necessary to verify the CLI
  // interface works correctly. No external input or command injection is
  // possible as all paths are resolved statically at test-time.
  const result = spawnSync(
    process.execPath,
    [path.join(skillRoot, 'bin', 'moltmotion-skill.js'), 'validate-state'],
    { cwd: skillRoot, encoding: 'utf8' }
  );

  assert.equal(result.status, 0, `stderr=${result.stderr}`);
  assert.match(result.stdout, /state validation passed/i);
});
