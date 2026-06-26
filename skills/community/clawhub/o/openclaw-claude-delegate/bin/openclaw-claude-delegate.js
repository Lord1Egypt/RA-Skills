#!/usr/bin/env node
const { spawnSync } = require('node:child_process');
const path = require('node:path');

const script = path.join(__dirname, '..', 'install.sh');
const args = process.argv.slice(2);
const command = args[0] || 'install';

if (command === 'install') {
  const result = spawnSync('bash', [script, ...args.slice(1)], { stdio: 'inherit' });
  process.exit(result.status ?? 1);
}

if (command === 'help' || command === '--help' || command === '-h') {
  console.log('Usage: openclaw-claude-delegate [install] [install options]');
  console.log('');
  console.log('Examples:');
  console.log('  npx openclaw-claude-delegate');
  console.log('  npx openclaw-claude-delegate install --force');
  process.exit(0);
}

console.error(`Unknown command: ${command}`);
process.exit(1);
