#!/usr/bin/env node
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { execFileSync } from 'node:child_process';

const tmpRoot = fs.mkdtempSync(path.join(os.tmpdir(), 'openclaw-cost-guard-'));
const configPath = path.join(tmpRoot, 'openclaw.json');
const config = {
  defaultModel: 'gpt-5',
  reasoning: { enabled: true },
  cron: { jobs: [{ name: 'nightly' }] },
  limits: { maxOutputTokens: 20000 },
  browser: { enabled: true }
};
fs.writeFileSync(configPath, JSON.stringify(config, null, 2));

let stdout = '';
let exitCode = 0;
try {
  stdout = execFileSync('node', ['scripts/cost-guard.mjs', '--config', configPath], {
    cwd: path.resolve(process.cwd()),
    encoding: 'utf8'
  });
} catch (error) {
  exitCode = error.status ?? 1;
  stdout = error.stdout?.toString() ?? '';
}
const data = JSON.parse(stdout);
assert.equal(exitCode, 1);
assert.equal(data.verdict, 'FAIL');
assert.ok(Array.isArray(data.findings) && data.findings.length > 0);
assert.ok(data.findings.some((item) => item.area === 'budget'));
assert.ok(Array.isArray(data.guardrails) && data.guardrails.length > 0);

console.log('cost-guard test: PASS');
