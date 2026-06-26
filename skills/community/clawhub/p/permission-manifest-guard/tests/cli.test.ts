import { describe, it, after } from 'node:test';
import assert from 'node:assert/strict';
import { execSync } from 'node:child_process';
import { resolve, join } from 'node:path';
import { readFileSync, unlinkSync, existsSync } from 'node:fs';

const CLI_PATH = resolve(import.meta.dirname, '..', 'src', 'cli.ts');
const FIXTURE_DIR = resolve(import.meta.dirname, 'fixtures', 'sample-skill');
const JSON_OUTPUT = join(FIXTURE_DIR, 'permission-manifest.json');

// Shared invocation command — uses tsx loader so no build step is needed.
const CMD = `node --import tsx ${CLI_PATH} ${FIXTURE_DIR}`;

describe('CLI integration', () => {
  // Clean up any JSON file written by test 2 so the fixture stays pristine.
  after(() => {
    if (existsSync(JSON_OUTPUT)) {
      unlinkSync(JSON_OUTPUT);
    }
  });

  it('valid directory prints markdown to stdout', () => {
    const stdout = execSync(CMD, { encoding: 'utf-8' });
    assert.ok(
      stdout.includes('# Permission Manifest'),
      `stdout must contain '# Permission Manifest', got: ${stdout.slice(0, 200)}`,
    );
    // At least one section heading below the title.
    assert.match(stdout, /^## .+/m, 'stdout must contain at least one ## section heading');
  });

  it('valid directory writes parseable JSON manifest file', () => {
    execSync(CMD, { encoding: 'utf-8' });
    assert.ok(existsSync(JSON_OUTPUT), `expected JSON file at ${JSON_OUTPUT}`);

    const raw = readFileSync(JSON_OUTPUT, 'utf-8');
    const parsed = JSON.parse(raw) as Record<string, unknown>;
    assert.ok('skill_name' in parsed, 'JSON manifest must have skill_name key');
    assert.ok('disposition' in parsed, 'JSON manifest must have disposition key');
  });

  it('missing argument exits with non-zero code and prints usage hint', () => {
    const noArgCmd = `node --import tsx ${CLI_PATH}`;
    try {
      execSync(noArgCmd, { encoding: 'utf-8', stdio: 'pipe' });
      assert.fail('CLI should have exited with non-zero code when no argument is provided');
    } catch (err: unknown) {
      // execSync throws when the child exits non-zero.
      const execErr = err as { status: number; stderr: string | Buffer };
      assert.ok(execErr.status !== 0, `expected non-zero exit code, got ${execErr.status}`);
      const stderr = typeof execErr.stderr === 'string'
        ? execErr.stderr
        : execErr.stderr.toString('utf-8');
      assert.ok(
        stderr.includes('Usage'),
        `stderr should contain usage hint, got: ${stderr.slice(0, 200)}`,
      );
    }
  });
});
