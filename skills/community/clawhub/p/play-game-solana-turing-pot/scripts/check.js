#!/usr/bin/env node
/**
 * check.js — Read unread events from the Turing Pot daemon.
 *
 * Prints unread events as a JSON array, then marks them as read.
 * Prints NOTHING if there are no unread events.
 *
 * This is intentional: OpenClaw cron hooks only wake the LLM when
 * this script produces output. Zero output = zero LLM calls.
 *
 * Usage:
 *   node check.js              # unread events only
 *   node check.js --all        # all events (read and unread)
 *   node check.js --chat 20    # last N chat messages for context
 *   node check.js --status     # daemon running state + session stats
 */

'use strict';

const fs   = require('fs');
const path = require('path');
const os   = require('os');

const DATA_DIR      = path.join(os.homedir(), '.turing-pot');
const EVENTS_FILE   = path.join(DATA_DIR, 'events.jsonl');
const CHAT_IN_FILE  = path.join(DATA_DIR, 'chat.jsonl');
const STAT_FILE     = path.join(DATA_DIR, 'session.json');
const PID_FILE      = path.join(DATA_DIR, 'player.pid');

const args    = process.argv.slice(2);
const hasFlag = f => args.includes(f);
const arg     = (flag, def) => { const i = args.indexOf(flag); return (i >= 0 && args[i+1]) ? args[i+1] : def; };

// ── --status ───────────────────────────────────────────────────────
if (hasFlag('--status')) {
  let stats = {};
  try { stats = JSON.parse(fs.readFileSync(STAT_FILE, 'utf8')); } catch {}
  let running = false;
  try {
    const pid = parseInt(fs.readFileSync(PID_FILE, 'utf8').trim());
    process.kill(pid, 0);
    running = true;
  } catch {}
  console.log(JSON.stringify({ running, ...stats }, null, 2));
  process.exit(0);
}

// ── --chat N ───────────────────────────────────────────────────────
if (hasFlag('--chat')) {
  const n = parseInt(arg('--chat', '20'));
  try {
    const lines = fs.readFileSync(CHAT_IN_FILE, 'utf8')
      .trim().split('\n').filter(Boolean).slice(-n)
      .map(l => { try { return JSON.parse(l); } catch { return null; } })
      .filter(Boolean);
    if (lines.length) console.log(JSON.stringify(lines, null, 2));
  } catch {}
  process.exit(0);
}

// ── Default: unread events (or --all) ─────────────────────────────
if (!fs.existsSync(EVENTS_FILE)) process.exit(0);

const raw = fs.readFileSync(EVENTS_FILE, 'utf8').trim();
if (!raw) process.exit(0);

const lines   = raw.split('\n').filter(Boolean);
const all     = hasFlag('--all');
const unread  = [];
const updated = [];

for (const line of lines) {
  try {
    const entry = JSON.parse(line);
    if (!entry.read || all) unread.push(entry);
    // Mark as read in the rewritten file
    updated.push(JSON.stringify({ ...entry, read: true }));
  } catch {
    updated.push(line); // keep malformed lines unchanged
  }
}

// Rewrite file with all entries marked read
fs.writeFileSync(EVENTS_FILE, updated.join('\n') + '\n');

// Only print (and therefore only wake the LLM) if there's something to act on
if (unread.length > 0) {
  console.log(JSON.stringify(unread, null, 2));

  // Remind the agent what to do with chat_prompt events
  const chatPrompts = unread.filter(e => e.type === 'chat_prompt');
  if (chatPrompts.length > 0) {
    console.log('\n---');
    console.log('For each chat_prompt event: read the "instruction" field, compose');
    console.log('one short in-character message, append to ~/.turing-pot/chat-out.jsonl');
    console.log('as: {"message": "your message here"}');
    console.log('The daemon sends it to game chat within 3 seconds. One sentence. No emojis.');
  }
}
