import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync, writeFileSync, mkdtempSync, rmSync, readdirSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const root = fileURLToPath(new URL('../../../', import.meta.url));
const script = fileURLToPath(new URL('./validate-config.mjs', import.meta.url));
const example = fileURLToPath(new URL('../assets/comparison.example.json', import.meta.url));

function validate(file, flags = []) {
  const child = spawnSync(process.execPath, [script, '--repo', root, file, ...flags], {
    encoding: 'utf8', timeout: 45_000,
  });
  if (child.error) throw child.error;
  return { status: child.status, output: JSON.parse(child.status === 0 ? child.stdout : child.stderr) };
}
function withModifiedExample(t, modify) {
  const dir = mkdtempSync(join(tmpdir(), 'mcp-token-lab-skill-'));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  const data = JSON.parse(readFileSync(example, 'utf8'));
  modify(data);
  const file = join(dir, 'scenario.json');
  writeFileSync(file, JSON.stringify(data));
  return file;
}

test('sample template imports and simulates with strict validation', () => {
  const r = validate(example, ['--simulate', '--strict']);
  assert.equal(r.status, 0);
  assert.equal(r.output.valid, true);
  assert.equal(r.output.simulated, true);
  assert.equal(r.output.plans, 2);
  assert.deepEqual(r.output.warnings, []);
  assert.ok(r.output.results.every(item => Number.isFinite(item.totalCost)));
});

test('packaged builtins stay in sync and all pass strict full simulation', () => {
  const sync = fileURLToPath(new URL('./sync-builtins.mjs', import.meta.url));
  const child = spawnSync(process.execPath, [sync, '--repo', root, '--check'], { encoding: 'utf8' });
  assert.equal(child.status, 0, child.stderr);
  const directory = new URL('../assets/examples/', import.meta.url);
  const files = readdirSync(directory, { recursive: true }).filter(file => file.endsWith('.json'));
  assert.ok(files.length > 0);
  for (const file of files) {
    const r = validate(fileURLToPath(new URL(file, directory)), ['--simulate', '--strict']);
    assert.equal(r.status, 0, file + ': ' + JSON.stringify(r.output));
    assert.equal(r.output.simulated, true);
    assert.ok(r.output.template.name && r.output.template.description);
    assert.deepEqual(r.output.warnings, []);
    assert.ok(r.output.results.every(item => Number.isFinite(item.totalCost)));
  }
});

test('plain configuration imports without a template wrapper', t => {
  const file = withModifiedExample(t, data => {
    const config = data.config;
    for (const key of Object.keys(data)) delete data[key];
    Object.assign(data, config);
  });
  const r = validate(file, ['--strict']);
  assert.equal(r.status, 0);
  assert.equal(r.output.valid, true);
  assert.equal(r.output.simulated, false);
  assert.equal(r.output.template, undefined);
});

test('strict mode catches unresolved, invalid and unpaired placeholders', t => {
  const file = withModifiedExample(t, data => {
    data.config.plans[0].description += ' {{missingVariable}} {{toolsTotalCount + 1}} {{unfinished';
  });
  const lenient = validate(file);
  assert.equal(lenient.status, 0);
  assert.ok(lenient.output.warnings.some(item => item.includes('missingVariable')));
  assert.ok(lenient.output.warnings.some(item => item.includes('toolsTotalCount + 1')));
  assert.ok(lenient.output.warnings.some(item => item.includes('unmatched double braces')));
  const strict = validate(file, ['--strict']);
  assert.notEqual(strict.status, 0);
  assert.equal(strict.output.valid, false);
});

test('full simulation detects formula errors after the first turn', t => {
  const file = withModifiedExample(t, data => {
    data.config.plans[0].simulation.flow.turn[0].token = '1 / (2 - turnIndex)';
  });
  assert.equal(validate(file, ['--strict']).status, 0);
  const r = validate(file, ['--simulate', '--strict']);
  assert.notEqual(r.status, 0);
  assert.match(r.output.error, /turnIndex|formula|flow\.turn|\u516c\u5f0f/i);
});

test('unrecognized command-line arguments fail', () => {
  const r = validate(example, ['--unknown']);
  assert.notEqual(r.status, 0);
  assert.equal(r.output.valid, false);
});
