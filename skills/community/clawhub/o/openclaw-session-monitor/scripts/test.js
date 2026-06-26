#!/usr/bin/env node
// test.js — dry-run: parse recent JSONL entries and print what would be sent
const fs = require('fs');
const path = require('path');
const { loadKeys, getTag, DIR } = require('./sessions');
const { parse } = require('./parser');
const { mergeMessages } = require('./formatter');

loadKeys();

const files = fs.readdirSync(DIR).filter(f => f.endsWith('.jsonl') && !f.includes('.deleted.'));
let total = 0;

for (const f of files) {
  const fp = path.join(DIR, f);
  const lines = fs.readFileSync(fp, 'utf8').split('\n').filter(Boolean);
  const sid = path.basename(fp, '.jsonl');
  const tag = getTag(sid);
  const entries = [];

  // take last 10 lines
  for (const raw of lines.slice(-10)) {
    try {
      const e = parse(JSON.parse(raw));
      if (e) entries.push(e);
    } catch {}
  }
  if (!entries.length) continue;

  const merged = mergeMessages(entries);
  console.log(`\n[${tag}]`);
  for (const m of merged) console.log(m);
  total += entries.length;
}

console.log(`\n--- ${total} entries from ${files.length} sessions ---`);
