#!/usr/bin/env node
// session-monitor v13 — multi-agent support
const fs = require('fs');
const path = require('path');
const { pushUpdate, freezeMessage } = require('./sender');
const { loadKeys, getTag, getAllDirs } = require('./sessions');
const { parse } = require('./parser');
const { buildMessage } = require('./formatter');

const POLL = 3000;
const MERGE_WINDOW = 1;
const MAX_MSG_LEN = 3500;

const sizes = new Map();
let currentWindow = null;
let accGroups = new Map();
let hasSentInWindow = false;

function getWindowKey() {
  const d = new Date();
  return `${d.getDate()}h${d.getHours()}s${Math.floor(d.getMinutes() / MERGE_WINDOW)}`;
}

function poll() {
  try {
    const newEntries = new Map();
    const allDirs = getAllDirs();

    for (const { name: agentName, dir } of allDirs) {
      let files;
      try {
        files = fs.readdirSync(dir).filter(f => f.endsWith('.jsonl') && !f.includes('.deleted.'));
      } catch { continue; }

      for (const f of files) {
        const fp = path.join(dir, f);
        const prev = sizes.get(fp) || 0;
        let size;
        try { size = fs.statSync(fp).size; } catch { continue; }
        if (!prev) { sizes.set(fp, size); continue; }
        if (size <= prev) { sizes.set(fp, size); continue; }

        try {
          const fd = fs.openSync(fp, 'r');
          const buf = Buffer.alloc(size - prev);
          fs.readSync(fd, buf, 0, buf.length, prev);
          fs.closeSync(fd);
          sizes.set(fp, size);
          const sid = path.basename(fp, '.jsonl');
          const tag = getTag(sid, agentName);
          for (const raw of buf.toString('utf8').split('\n')) {
            if (!raw.trim()) continue;
            try {
              const e = parse(JSON.parse(raw));
              if (e) {
                if (!newEntries.has(tag)) newEntries.set(tag, []);
                newEntries.get(tag).push(e);
              }
            } catch {}
          }
        } catch { sizes.set(fp, size); }
      }
    }

    if (!newEntries.size) return;

    const window = getWindowKey();
    if (window !== currentWindow) {
      if (hasSentInWindow) freezeMessage();
      currentWindow = window;
      accGroups = new Map();
      hasSentInWindow = false;
    }

    for (const [tag, entries] of newEntries) {
      if (!accGroups.has(tag)) accGroups.set(tag, []);
      accGroups.get(tag).push(...entries);
    }

    const msg = buildMessage(accGroups);
    if (!msg) return;

    if (hasSentInWindow && msg.length > MAX_MSG_LEN) {
      freezeMessage();
      accGroups = new Map();
      hasSentInWindow = false;
      for (const [tag, entries] of newEntries) {
        accGroups.set(tag, [...entries]);
      }
      const freshMsg = buildMessage(accGroups);
      if (freshMsg) {
        pushUpdate(freshMsg, true);
        hasSentInWindow = true;
      }
    } else {
      pushUpdate(msg, !hasSentInWindow);
      hasSentInWindow = true;
    }
  } catch (e) { console.error('[poll]', e.message); }
}

// PID file
const PID_FILE = path.join(__dirname, '.pid');
fs.writeFileSync(PID_FILE, String(process.pid));
process.on('exit', () => { try { fs.unlinkSync(PID_FILE); } catch {} });
process.on('SIGINT', () => process.exit());
process.on('SIGTERM', () => process.exit());

// Start
loadKeys();
setInterval(loadKeys, POLL * 5);
poll();
setInterval(poll, POLL);
pushUpdate('\u{1F5A5}\uFE0F <b>Monitor v13</b> started — tracking: ' + getAllDirs().map(a => a.name).join(', '), true);
