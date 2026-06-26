#!/usr/bin/env node

import { spawnSync } from 'node:child_process';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

function usage() {
  console.error('Usage: nlm.mjs <command> [args...]');
  console.error('Examples:');
  console.error('  nlm.mjs login');
  console.error('  nlm.mjs notebook list');
  console.error('  nlm.mjs source add <notebook-id> --url "https://example.com" --wait');
  console.error('  nlm.mjs slides create <notebook-id> --confirm');
  console.error('  nlm.mjs studio status <notebook-id>');
  console.error('  nlm.mjs download slide-deck <notebook-id> --id <artifact-id> --format pdf --output slides.pdf');
  process.exit(2);
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === '-h' || args[0] === '--help') usage();

const __filename = fileURLToPath(import.meta.url);
const skillDir = path.resolve(path.dirname(__filename), '..');
const localVenvBin = path.join(skillDir, '.venvs', 'nlm-mcp', 'bin');
const localVenvNlm = path.join(localVenvBin, 'nlm');
const configuredBin = process.env.NLM_BIN;

const env = { ...process.env };
let command = 'nlm';

if (configuredBin) {
  command = configuredBin;
} else if (existsSync(localVenvNlm)) {
  command = localVenvNlm;
} else {
  env.PATH = `${localVenvBin}:${env.PATH || ''}`;
}

const result = spawnSync(command, args, { stdio: 'inherit', env });

if (result.error) {
  console.error(`Failed to run ${command}: ${result.error.message}`);
  console.error('If nlm is not installed, read references/install-and-auth.md.');
  process.exit(1);
}

process.exit(result.status ?? 1);
