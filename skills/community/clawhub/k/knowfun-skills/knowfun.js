#!/usr/bin/env node
/**
 * Knowfun CLI for OpenClaw and Claude Code
 */

import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { spawn } from 'child_process';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const [command, ...args] = process.argv.slice(2);

if (!command) {
  console.log('Usage: knowfun <command> [args]');
  console.log('');
  console.log('Commands:');
  console.log('  create <type> <content>   Create educational content (course/poster/game/film)');
  console.log('  status <taskId>           Check task processing status');
  console.log('  detail <taskId>           Get detailed task results and content URL');
  console.log('  list [limit] [offset]     List recent tasks');
  console.log('  credits                   Check credit balance');
  console.log('  schema                    Get configuration schema');
  console.log('  usage [page] [pageSize]   Get usage statistics');
  process.exit(1);
}

const scriptPath = join(__dirname, 'scripts', 'knowfun-cli.sh');
const child = spawn('bash', [scriptPath, command, ...args], {
  stdio: 'inherit',
  env: process.env
});

child.on('exit', (code) => {
  process.exit(code || 0);
});
