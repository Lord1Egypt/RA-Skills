#!/usr/bin/env node

// OpenClaw Memory Auto Plugin
// Entry point for auto-archive heartbeat task

import { spawn } from 'child_process';
import { readFile, writeFile, mkdir } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Config paths (relative to workspace)
const MEMORY_DIR = join(process.env.OPENCLAW_WORKSPACE || process.cwd(), 'memory');
const LOG_DIR = join(process.env.OPENCLAW_WORKSPACE || process.cwd(), 'logs');
const ARCHIVE_SCRIPT = join(__dirname, 'archive.ps1');
const REFINE_SCRIPT = join(__dirname, 'refine.ps1');

// Ensure log dir exists
await mkdir(LOG_DIR, { recursive: true });

// Logger
function log(msg) {
  const ts = new Date().toISOString();
  console.log(`[${ts}] ${msg}`);
}

// Main logic: archive yesterday's chat
async function archiveYesterday() {
  log('=== START ARCHIVE ===');
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  const yStr = yesterday.toISOString().split('T')[0];
  const dailyFile = join(MEMORY_DIR, `${yStr}.md`);

  log(`Check: ${yStr}`);
  try {
    await readFile(dailyFile, 'utf8');
    log('Exists, skip');
    return { skipped: true };
  } catch {
    // continue
  }

  // Find transcript
  const transcriptDir = 'C:\\Users\\42517\\.openclaw\\agents\\main\\sessions';
  // Use PowerShell script to do the heavy lifting
  const psArgs = [
    '-NoProfile',
    '-ExecutionPolicy', 'Bypass',
    '-File', ARCHIVE_SCRIPT,
    '-Workspace', process.env.OPENCLAW_WORKSPACE || process.cwd()
  ];

  return new Promise((resolve, reject) => {
    const ps = spawn('powershell.exe', psArgs, { stdio: 'inherit' });
    ps.on('close', (code) => {
      if (code === 0) {
        log('Archive completed');
        resolve({ skipped: false });
      } else {
        reject(new Error(`PowerShell exit code ${code}`));
      }
    });
  });
}

// Command line handling
const args = process.argv.slice(2);
if (args.includes('--archive')) {
  archiveYesterday()
    .then(res => process.exit(0))
    .catch(err => {
      log(`ERROR: ${err.message}`);
      process.exit(1);
    });
} else {
  log('Usage: node index.js --archive');
  process.exit(1);
}
