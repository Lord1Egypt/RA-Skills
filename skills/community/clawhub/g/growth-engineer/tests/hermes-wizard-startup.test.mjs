import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { join, resolve } from 'node:path';
import test from 'node:test';

const skillRoot = resolve(import.meta.dirname, '..');

test('Hermes startup instructions tell chat agents to hand off a full wizard command', () => {
  const skill = readFileSync(join(skillRoot, 'SKILL.md'), 'utf8');

  assert.match(skill, /## Hermes Startup Override/);
  assert.match(skill, /npx -y @analyticscli\/growth-engineer wizard --connectors/);
  assert.match(skill, /Do not satisfy those messages by only installing `analyticscli`/);
  assert.match(skill, /do not start the interactive wizard process yourself/i);
  assert.match(skill, /Post-Install Reply Contract/);
  assert.match(skill, /Mac mini/);
  assert.match(skill, /Run this in your VPS\/host shell and paste secrets only there/);
});

test('runtime auth remediation does not route AnalyticsCLI setup to standalone login', () => {
  const runtimeFiles = [
    'scripts/openclaw-growth-preflight.mjs',
    'scripts/openclaw-growth-start.mjs',
  ];

  for (const file of runtimeFiles) {
    const source = readFileSync(join(skillRoot, file), 'utf8');
    assert.doesNotMatch(source, /analyticscli login/);
    assert.match(source, /npx -y @analyticscli\/growth-engineer wizard --connectors analytics/);
  }
});
