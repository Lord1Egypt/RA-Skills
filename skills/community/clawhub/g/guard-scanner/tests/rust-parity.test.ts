import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
import { describe, it, assert, beforeEach, afterEach, vi } from 'vitest';

import { execFileSync  } from 'node:child_process';
import path  from 'node:path';

describe('Rust parity harness', () => {
    it('matches TypeScript risk scoring fixtures', () => {
        const root = path.join(__dirname, '..');
        const output = execFileSync('npx', ['tsx', 'scripts/rust-parity.ts'], {
            cwd: root,
            encoding: 'utf8',
        });
        assert.match(output, /Rust parity: 3\/3 matched/);
    });
});
