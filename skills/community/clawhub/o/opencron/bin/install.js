#!/usr/bin/env node
'use strict';

const { execFileSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const REPO = 'https://github.com/firstfloris/opencron-skill.git';
const SKILL_DIR = path.join(process.cwd(), 'skills', 'opencron');

const log = (msg) => console.log(`\x1b[32m⠿\x1b[0m ${msg}`);
const err = (msg) => { console.error(`\x1b[31m⠻\x1b[0m ${msg}`); process.exit(1); };

const args = process.argv.slice(2);
const cmd = args[0] || 'add';

if (cmd === 'add') {
  if (fs.existsSync(SKILL_DIR)) {
    err(`${SKILL_DIR} already exists. Remove it first or run: npx opencron-skill update`);
  }

  log('Cloning opencron-skill...');
  execFileSync('git', ['clone', '--depth', '1', REPO, SKILL_DIR], { stdio: 'inherit' });

  const gitDir = path.join(SKILL_DIR, '.git');
  if (fs.existsSync(gitDir)) {
    fs.rmSync(gitDir, { recursive: true, force: true });
  }

  log('Deploying dashboard...');
  try {
    execFileSync('python3', [path.join(SKILL_DIR, 'update_canvas.py')], { stdio: 'inherit' });
  } catch (e) {
    log('Skipped deploy (python3 not available or no OpenClaw install found)');
  }

  console.log('');
  log('Installed to skills/opencron');
  log('Start background sync:  nohup sh skills/opencron/watch_sync.sh &');
  log('Open demo:              open skills/opencron/demo.html');
  console.log('');
} else if (cmd === 'update') {
  if (!fs.existsSync(SKILL_DIR)) {
    err(`${SKILL_DIR} not found. Run: npx opencron-skill add`);
  }

  log('Updating dashboard from GitHub...');
  try {
    execFileSync('python3', [path.join(SKILL_DIR, 'update_canvas.py')], { stdio: 'inherit' });
  } catch (e) {
    err('Update failed: ' + e.message);
  }

  log('Dashboard updated');
} else {
  console.log('Usage: npx opencron-skill [add|update]');
  console.log('');
  console.log('  add     Install the OpenCron skill (default)');
  console.log('  update  Re-fetch the dashboard HTML from GitHub');
}
