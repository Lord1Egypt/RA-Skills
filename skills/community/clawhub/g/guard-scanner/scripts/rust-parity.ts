import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
import path from 'node:path';
import { execFileSync } from 'node:child_process';
import { calculateRisk }  from '../src/core/risk-engine';

const ROOT = path.join(__dirname, '..');
const MANIFEST = path.join(ROOT, 'rust', 'guard-scan-core', 'Cargo.toml');

const fixtures = [
    { name: 'empty', findings: [] },
    { name: 'single-critical', findings: [{ id: 'A', severity: 'CRITICAL', confidence: 0.95, category: 'prompt-injection' }] },
    {
        name: 'credential-exfil-chain',
        findings: [
            { id: 'A', severity: 'HIGH', confidence: 0.82, category: 'credential-handling' },
            { id: 'B', severity: 'HIGH', confidence: 0.82, category: 'exfiltration' },
        ],
    },
];

const payload = fixtures.map((fixture) => ({
    name: fixture.name,
    expected: calculateRisk(fixture.findings.map((finding) => ({
        ...finding,
        cat: finding.category,
    }))),
    findings: fixture.findings,
}));

const raw = execFileSync('cargo', ['run', '--quiet', '--manifest-path', MANIFEST], {
    cwd: ROOT,
    input: JSON.stringify(payload),
    encoding: 'utf8',
});

const actual = JSON.parse(raw);
let matched = 0;
for (const result of actual.results) {
    if (result.expected === result.actual) matched++;
}

if (matched !== payload.length) {
    throw new Error(`Rust parity mismatch: ${JSON.stringify(actual.results)}`);
}

console.log(`Rust parity: ${matched}/${payload.length} matched`);
