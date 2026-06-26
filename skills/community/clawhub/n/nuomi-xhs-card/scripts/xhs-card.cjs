#!/usr/bin/env node
const { spawnSync } = require('node:child_process');
const path = require('node:path');

const cliPath = path.resolve(__dirname, 'src', 'cli.ts');
const tsxLoaderPath = path.resolve(__dirname, 'node_modules', 'tsx', 'dist', 'loader.mjs');

const result = spawnSync(process.execPath, ['--import', tsxLoaderPath, cliPath, ...process.argv.slice(2)], {
  stdio: 'inherit'
});

process.exit(result.status === null ? 1 : result.status);
