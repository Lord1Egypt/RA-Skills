#!/usr/bin/env node

/**
 * pixel-agents — CLI entry point for the Pixel Agents Dashboard.
 *
 * Usage:
 *   npx pixel-agents-dashboard    # run from npm
 *   pixel-agents                  # if installed globally
 *
 * First run (no config): opens setup wizard at http://localhost:5070
 * With config: starts the dashboard server
 */

'use strict';

const { spawn } = require('child_process');
const path = require('path');

const projectRoot = path.resolve(__dirname, '..');
const serverEntry = path.resolve(projectRoot, 'server', 'index.ts');

// tsx handles TypeScript execution without a separate compile step.
// It's included as a dependency, so npx finds it in node_modules/.bin/.
const child = spawn(
  process.execPath, // node binary
  [
    path.resolve(projectRoot, 'node_modules', '.bin', 'tsx'),
    serverEntry,
  ],
  {
    cwd: process.cwd(), // run from user's CWD so config file is found there
    stdio: 'inherit',
    env: {
      ...process.env,
      // Pass project root so the server can find bundled assets
      PIXEL_AGENTS_ROOT: projectRoot,
    },
  },
);

child.on('error', (err) => {
  if (err.code === 'ENOENT') {
    // tsx not found — try npx fallback
    const fallback = spawn('npx', ['tsx', serverEntry], {
      cwd: process.cwd(),
      stdio: 'inherit',
      env: { ...process.env, PIXEL_AGENTS_ROOT: projectRoot },
      shell: true,
    });
    fallback.on('exit', (code) => process.exit(code ?? 1));
    process.on('SIGINT', () => fallback.kill('SIGINT'));
    process.on('SIGTERM', () => fallback.kill('SIGTERM'));
    return;
  }
  console.error('Failed to start:', err.message);
  process.exit(1);
});

child.on('exit', (code) => process.exit(code ?? 0));

process.on('SIGINT', () => child.kill('SIGINT'));
process.on('SIGTERM', () => child.kill('SIGTERM'));
