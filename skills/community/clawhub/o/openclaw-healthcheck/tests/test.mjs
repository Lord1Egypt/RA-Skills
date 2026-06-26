import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const tmp = fs.mkdtempSync(path.join(os.tmpdir(), 'openclaw-healthcheck-'));
const binDir = path.join(tmp, 'bin');
fs.mkdirSync(binDir, { recursive: true });

const statusStub = `#!/bin/sh
echo 'OpenClaw status: OK'
`;
fs.writeFileSync(path.join(binDir, 'openclaw'), statusStub, { mode: 0o755 });

const scriptPath = fileURLToPath(new URL('../scripts/healthcheck.mjs', import.meta.url));
const env = {
  ...process.env,
  PATH: `${binDir}:${process.env.PATH || ''}`,
  HOME: tmp,
};

fs.mkdirSync(path.join(tmp, '.openclaw'), { recursive: true });
fs.writeFileSync(
  path.join(tmp, '.openclaw', 'openclaw.json'),
  JSON.stringify({ gateway: { bind: '127.0.0.1:18789' } }, null, 2)
);

const out = execFileSync(process.execPath, [scriptPath], {
  encoding: 'utf8',
  env,
});

const result = JSON.parse(out);
assert.ok(typeof result.score === 'number');
assert.ok(['PASS', 'WARN', 'FAIL'].includes(result.verdict));
assert.ok(Array.isArray(result.findings));
assert.ok(Array.isArray(result.recommendations));
assert.ok(result.evidence);

console.log(`healthcheck test: ${result.verdict}`);
