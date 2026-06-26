#!/usr/bin/env node
import fs from 'fs';
import path from 'path';

const args = process.argv.slice(2);
const dryRun = args.includes('--dry-run');
const positional = args.filter(arg => arg !== '--dry-run');
const [target, text] = positional;
if (!target || !text) {
  console.error('Usage: node promote-learning.mjs <workflow|tools|behavior|obsidian> <text> [--dry-run]');
  process.exit(2);
}

const workspace = process.env.WORKSPACE || path.join(process.env.HOME, '.openclaw/workspace');
const obsidianDir = process.env.OBSIDIAN_LEARNINGS_DIR || path.join(workspace, '.learnings', 'exports', 'obsidian');
const targets = {
  workflow: path.join(workspace, 'AGENTS.md'),
  tools: path.join(workspace, 'TOOLS.md'),
  behavior: path.join(workspace, 'SOUL.md'),
  obsidian: path.join(obsidianDir, `${new Date().toISOString().slice(0,10)}-learning.md`)
};

const file = targets[target];
if (!file) {
  console.error('target must be workflow|tools|behavior|obsidian');
  process.exit(2);
}

console.error(`[promote-learning] target=${target}`);
console.error(`[promote-learning] path=${file}`);
if (dryRun) {
  console.log(file);
  process.exit(0);
}

fs.mkdirSync(path.dirname(file), { recursive: true });
fs.appendFileSync(file, `\n- ${text}\n`);
console.log(file);
