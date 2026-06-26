#!/usr/bin/env node
/**
 * Build validation script for @hodl-dance/skill.
 *
 * Since this is a pure JavaScript project (no TypeScript, no bundler),
 * the "build" step performs syntax validation on all source files
 * using Node's built-in --check flag.
 *
 * This provides a consistent `npm run build` experience across
 * Windows, macOS, and Linux (including WSL).
 */

const { execSync } = require('child_process');
const path = require('path');

const SOURCE_FILES = [
  'src/index.js',
  'src/lib/api.js',
  'src/lib/chain.js',
  'src/lib/output.js',
  'src/lib/validators.js',
  'src/commands/get-tokens.js',
  'src/commands/get-token.js',
  'src/commands/get-trades.js',
  'src/commands/quote.js',
  'src/commands/buy-token.js',
  'src/commands/sell-token.js',
  'src/commands/create-token.js',
];

let hasErrors = false;

console.log('Running build checks...\n');

for (const file of SOURCE_FILES) {
  const fullPath = path.join(__dirname, '..', file);

  try {
    execSync(`node --check "${fullPath}"`, { stdio: 'pipe' });
    console.log(`  ✓  ${file}`);
  } catch (error) {
    hasErrors = true;
    console.error(`  ✗  ${file}`);
    if (error.stdout) {
      console.error(error.stdout.toString());
    }
    if (error.stderr) {
      console.error(error.stderr.toString());
    }
  }
}

console.log('');

if (hasErrors) {
  console.error('Build failed: one or more files have syntax errors.');
  process.exit(1);
} else {
  console.log('Build check passed (pure JavaScript project - no compilation required).');
  process.exit(0);
}
