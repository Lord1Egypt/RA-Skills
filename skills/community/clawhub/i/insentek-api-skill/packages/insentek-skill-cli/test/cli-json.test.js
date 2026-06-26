import assert from 'node:assert/strict';
import { spawnSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { describe, it } from 'node:test';

const packageRoot = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const binPath = path.join(packageRoot, 'bin/insentek-api-skill.js');

function runCli(args) {
  return spawnSync(process.execPath, [binPath, ...args], {
    cwd: packageRoot,
    encoding: 'utf8',
  });
}

describe('CLI --json output', () => {
  it('prints JSON for info --json', () => {
    const result = runCli(['info', '--json']);
    assert.equal(result.status, 0, result.stderr);

    const payload = JSON.parse(result.stdout.trim());
    assert.equal(payload.ok, true);
    assert.equal(payload.command, 'info');
    assert.equal(payload.package.name, '@insentek/openapi-skill');
    assert.ok(Array.isArray(payload.runtimes));
    assert.ok(payload.environment, 'environment must be present');
    assert.ok(payload.environment.python, 'environment.python must be present');
    assert.equal(typeof payload.environment.python.command, 'string');
    assert.equal(typeof payload.environment.python.ok, 'boolean');

    const firstScope = payload.runtimes[0]?.scopes?.[0];
    assert.ok(firstScope, 'at least one runtime scope must be present');
    assert.equal(typeof firstScope.installed, 'boolean', 'scope must expose installed flag');
    assert.ok(firstScope.python, 'scope must expose python info');
    assert.equal(typeof firstScope.python.command, 'string');
  });

  it('prints JSON for status --json', () => {
    const result = runCli(['status', '-r', 'claude', '--json']);
    assert.equal(result.status, 0, result.stderr);

    const payload = JSON.parse(result.stdout.trim());
    assert.equal(payload.ok, true);
    assert.equal(payload.command, 'status');
    assert.ok(Array.isArray(payload.results));
    assert.equal(payload.results[0].runtimeId, 'claude');
    assert.ok(payload.results[0].python, 'status entry must expose python info');
    assert.equal(typeof payload.results[0].installed, 'boolean');
  });

  it('prints JSON error when --json install lacks --yes', () => {
    const result = runCli(['install', '-r', 'claude', '--json']);
    assert.equal(result.status, 1);

    const payload = JSON.parse(result.stderr.trim());
    assert.equal(payload.ok, false);
    assert.equal(payload.error.code, 'NON_INTERACTIVE_REQUIRED');
  });

  it('prints JSON for doctor --json', () => {
    const result = runCli(['doctor', '-r', 'claude', '--json']);
    assert.ok(result.stdout.trim().startsWith('{'), result.stdout || result.stderr);

    const payload = JSON.parse(result.stdout.trim());
    assert.equal(payload.command, 'doctor');
    assert.ok(Array.isArray(payload.checks));
    assert.equal(typeof payload.allPassed, 'boolean');
  });
});
