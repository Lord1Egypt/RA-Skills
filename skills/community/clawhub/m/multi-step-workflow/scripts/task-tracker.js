#!/usr/bin/env node
/**
 * task-tracker — Track steps for complex tasks
 * 
 * Usage:
 *   node task-tracker.js new  "<task>" "<step1|step2|step3>"
 *   node task-tracker.js done "<task>" <step_number>
 *   node task-tracker.js list
 */

import { readFileSync, writeFileSync, mkdirSync, existsSync, readdirSync, chmodSync } from 'fs';
import { resolve, join } from 'path';

import { getTempDir } from './path-resolver.js';

const TRACKER_DIR = join(getTempDir(), 'tasks');
if (!existsSync(TRACKER_DIR)) {
  mkdirSync(TRACKER_DIR, { recursive: true });
}

function taskFile(name) {
  return join(TRACKER_DIR, Buffer.from(name).toString('hex') + '.json');
}

function load(name) {
  const f = taskFile(name);
  if (!existsSync(f)) return null;
  return JSON.parse(readFileSync(f, 'utf8'));
}

function save(name, data) {
  const f = taskFile(name);
  writeFileSync(f, JSON.stringify(data, null, 2));
  try {
    chmodSync(f, 0o600);
  } catch (e) {
    // Failsafe
  }
}

const [cmd, arg1, arg2] = process.argv.slice(2);

if (!cmd) {
  console.log('Commands: new, done, list');
  process.exit(0);
}

if (cmd === 'new') {
  if (!arg1 || !arg2) { console.log('Usage: new "<task>" "<step1|step2|...>"'); process.exit(1); }
  const steps = arg2.split('|').map(s => s.trim()).filter(Boolean);
  save(arg1, { task: arg1, steps, done: [], createdAt: new Date().toISOString() });
  console.log(`[OK] Created "${arg1}" with ${steps.length} steps.`);
  steps.forEach((s, i) => console.log(`  ⏳ ${i + 1}. ${s}`));
}
else if (cmd === 'done') {
  if (!arg1 || !arg2) { console.log('Usage: done "<task>" <step_number>'); process.exit(1); }
  const data = load(arg1);
  if (!data) { console.log(`Task "${arg1}" not found.`); process.exit(1); }
  const idx = parseInt(arg2, 10) - 1;
  if (idx < 0 || idx >= data.steps.length) { console.log(`Invalid step number.`); process.exit(1); }
  if (!data.done.includes(idx)) data.done.push(idx);
  save(arg1, data);
  const remaining = data.steps.length - data.done.length;
  console.log(`[OK] Step ${idx + 1} done. ${remaining} remaining.`);
  if (remaining === 0) console.log(`[DONE] All steps completed!`);
}
else if (cmd === 'list') {
  const files = readdirSync(TRACKER_DIR).filter(f => f.endsWith('.json'));
  if (files.length === 0) { console.log('No tracked tasks.'); process.exit(0); }
  files.forEach(f => {
    const data = JSON.parse(readFileSync(join(TRACKER_DIR, f), 'utf8'));
    const progress = `${data.done.length}/${data.steps.length}`;
    console.log(`\n📋 ${data.task} [${progress}]`);
    data.steps.forEach((s, i) => {
      const mark = data.done.includes(i) ? '✅' : '⏳';
      console.log(`  ${mark} ${i + 1}. ${s}`);
    });
  });
}
else {
  console.log(`Unknown command: ${cmd}`);
  process.exit(1);
}
