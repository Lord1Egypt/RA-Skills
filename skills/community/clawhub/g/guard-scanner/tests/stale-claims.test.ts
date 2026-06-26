import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
import { describe, it, assert, beforeEach, afterEach, vi } from 'vitest';

import fs  from 'node:fs';
import path  from 'node:path';

const ROOT = path.join(__dirname, '..');
const DOCS = ['README.md', 'README_ja.md', 'SKILL.md', 'CHANGELOG.md'];
const BANNED = [
    /fully OpenClaw-compatible/i,
    /dist\/runtime-plugin\.js/,
    /test\/manifest\.test\.js/,
    /OpenClaw `v2026\.3\.12`/,
];

describe('stale compatibility claims', () => {
    for (const file of DOCS) {
        it(`${file} omits stale OpenClaw compatibility claims`, () => {
            const content = fs.readFileSync(path.join(ROOT, file), 'utf8');
            for (const regex of BANNED) {
                assert.equal(regex.test(content), false, `${file} should not contain ${regex}`);
            }
        });
    }
});
