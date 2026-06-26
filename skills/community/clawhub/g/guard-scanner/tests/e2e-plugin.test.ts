import { fileURLToPath } from 'node:url';
import { dirname } from 'node:path';
const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
// @ts-nocheck
/**
 * E2E Plugin Test — guard-scanner OpenClaw plugin integration
 *
 * Tests the actual package surface that OpenClaw discovers:
 * - package.json exposes openclaw.extensions
 * - dist/openclaw-plugin.mjs exists after build
 * - openclaw.plugin.json keeps the same plugin id
 */

import { describe, it, assert, beforeEach, afterEach, vi } from 'vitest';

import path  from 'path';
import fs  from 'fs';
import pkg  from '../package.json';
import manifest  from '../openclaw.plugin.json';

const PLUGIN_PATH = path.join(__dirname, '..', 'dist', 'openclaw-plugin.mjs');

describe('E2E Plugin: Package surface', () => {
    it('package.json should declare official openclaw.extensions discovery metadata', () => {
        assert.deepEqual(pkg.openclaw.extensions, ['./dist/openclaw-plugin.mjs']);
    });

    it('package.json should publish explicit dual-package exports', () => {
        assert.equal(pkg.exports['.'].import, './dist/index.mjs');
        assert.equal(pkg.exports['.'].require, './dist/index.cjs');
        assert.equal(pkg.exports['./plugin'].require, './dist/openclaw-plugin.cjs');
        assert.equal(pkg.exports['./mcp'].import, './dist/mcp-server.mjs');
    });

    it('compiled plugin entry should exist after build', () => {
        assert.ok(fs.existsSync(PLUGIN_PATH), `compiled plugin should exist at ${PLUGIN_PATH}`);
    });

    it('compiled public entrypoints should exist after build', () => {
        for (const relPath of [
            '../guard-scanner',
            '../dist/index.cjs',
            '../dist/index.mjs',
            '../dist/mcp-server.cjs',
            '../dist/mcp-server.mjs',
            '../dist/openclaw-plugin.cjs',
            '../dist/openclaw-plugin.mjs',
            '../dist/cli.cjs',
            '../dist/types.d.ts',
        ]) {
            assert.ok(fs.existsSync(path.join(__dirname, relPath)), `compiled entry should exist at ${relPath}`);
        }
    });

    it('manifest id should match the public plugin id', () => {
        assert.equal(manifest.id, 'guard-scanner');
    });

    it('package.json should expose the stable CLI launcher', () => {
        assert.equal(pkg.bin['guard-scanner'], 'guard-scanner');
        assert.ok(fs.existsSync(path.join(__dirname, '..', 'guard-scanner')));
    });
});
