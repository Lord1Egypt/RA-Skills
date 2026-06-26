#!/usr/bin/env node
/**
 * memory-supersede.js
 * Mark a memory entry as superseded by a new one.
 * Creates a temporal chain: old fact → validUntil + supersededBy → new fact.
 *
 * Usage:
 *   node scripts/memory-supersede.js --old "Project Alpha: awaiting outcome" --new "Project Alpha: offer accepted" [--when "2026-04-01"]
 *
 * This will:
 *   1. Find the old entry (fuzzy match)
 *   2. Set its validUntil to now (or --when)
 *   3. Create or find the new entry
 *   4. Set the old entry's supersededBy to the new entry's key
 *   5. Set the new entry's validFrom to now (or --when)
 *
 * Flags:
 *   --old    <text>   The fact that is no longer true (fuzzy matched)
 *   --new    <text>   The fact that replaces it (fuzzy matched or created)
 *   --when   <date>   ISO date when the change happened (default: now)
 *   --dry-run         Preview without writing
 */

'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const WORKSPACE = path.resolve(__dirname, '..');
const META_PATH = path.join(WORKSPACE, 'memory', 'memory-meta.json');

const DRY_RUN = process.argv.includes('--dry-run');

function hashKey(line) {
  return crypto.createHash('md5').update(line.substring(0, 20)).digest('hex').substring(0, 12);
}

function normalise(s) {
  return s.toLowerCase().replace(/\s+/g, ' ').trim();
}

function findBestMatch(text, entries) {
  const norm = normalise(text);

  // Exact hash
  const key = hashKey(text);
  if (entries[key]) return { key, entry: entries[key], method: 'hash' };

  // Substring
  for (const [k, e] of Object.entries(entries)) {
    if (normalise(e.key).includes(norm) || norm.includes(normalise(e.key))) {
      return { key: k, entry: e, method: 'substring' };
    }
  }

  // Jaccard
  const words = new Set(norm.split(/\W+/).filter(Boolean));
  let bestKey = null, bestScore = 0, bestEntry = null;
  for (const [k, e] of Object.entries(entries)) {
    const eWords = new Set(normalise(e.key).split(/\W+/).filter(Boolean));
    const inter = [...words].filter(w => eWords.has(w)).length;
    const union = new Set([...words, ...eWords]).size;
    const score = union > 0 ? inter / union : 0;
    if (score > bestScore) { bestScore = score; bestKey = k; bestEntry = e; }
  }

  if (bestScore >= 0.25 && bestKey) {
    return { key: bestKey, entry: bestEntry, method: `fuzzy(${bestScore.toFixed(2)})` };
  }
  return null;
}

function parseArgs(argv) {
  const args = { old: null, new: null, when: null };
  let i = 2;
  while (i < argv.length) {
    if (argv[i] === '--old' && argv[i + 1]) args.old = argv[++i];
    else if (argv[i] === '--new' && argv[i + 1]) args.new = argv[++i];
    else if (argv[i] === '--when' && argv[i + 1]) args.when = argv[++i];
    i++;
  }
  return args;
}

function main() {
  const args = parseArgs(process.argv);
  if (!args.old || !args.new) {
    console.error('Usage: memory-supersede.js --old "<old fact>" --new "<new fact>" [--when <date>]');
    process.exit(1);
  }

  if (!fs.existsSync(META_PATH)) {
    console.error('❌ memory-meta.json not found. Run memory-bootstrap.js first.');
    process.exit(1);
  }

  const meta = JSON.parse(fs.readFileSync(META_PATH, 'utf8'));
  const when = args.when ? new Date(args.when).toISOString() : new Date().toISOString();

  // Find old entry
  const oldMatch = findBestMatch(args.old, meta.entries);
  if (!oldMatch) {
    console.error(`❌ Could not find old entry matching: "${args.old}"`);
    process.exit(1);
  }

  console.log(`📌 Old entry [${oldMatch.method}]: "${oldMatch.entry.key}"`);

  // Find or create new entry
  let newMatch = findBestMatch(args.new, meta.entries);
  let newKey;

  if (newMatch) {
    newKey = newMatch.key;
    console.log(`📌 New entry [${newMatch.method}]: "${newMatch.entry.key}"`);
  } else {
    newKey = hashKey(args.new);
    meta.entries[newKey] = {
      key: args.new.substring(0, 60).trim(),
      created: when,
      lastConfirmed: when,
      lastRecalled: null,
      recallCount: 0,
      tier: 'hot',
      source: 'conversation',
      decayScore: 1.0,
      validFrom: when,
      validUntil: null,
      supersededBy: null,
    };
    console.log(`➕ Created new entry: "${args.new.substring(0, 60)}"`);
  }

  // Update old entry
  oldMatch.entry.validUntil = when;
  oldMatch.entry.supersededBy = newKey;

  // Update new entry validFrom if it exists
  if (newMatch) {
    newMatch.entry.validFrom = newMatch.entry.validFrom || when;
  }

  console.log(`\n🔗 Chain: ${oldMatch.key} → ${newKey}`);
  console.log(`   validUntil: ${when}`);

  if (DRY_RUN) {
    console.log('\n🔍 DRY RUN — no files written.');
    return;
  }

  fs.writeFileSync(META_PATH, JSON.stringify(meta, null, 2) + '\n', 'utf8');
  console.log('\n💾 memory-meta.json saved.');
}

main();
