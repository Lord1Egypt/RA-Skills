#!/usr/bin/env node
/**
 * memory-recall-logger.js
 * Logs memory recall events — updates recallCount and lastRecalled for matched entries.
 *
 * Usage:
 *   node scripts/memory-recall-logger.js --query "dev server IP" --matches "Dev server: user@203.0.113.10"
 *
 * Multiple --matches flags are supported:
 *   node scripts/memory-recall-logger.js --query "IP" \
 *     --matches "Dev server: user@203.0.113.10" \
 *     --matches "SSH host: my-server"
 *
 * Flags:
 *   --query   <string>    The search query that triggered the recall
 *   --matches <string>    A matched line from MEMORY.md (repeatable)
 *   --dry-run             Print what would change without writing
 */

'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const WORKSPACE = path.resolve(__dirname, '..');
const META_PATH = path.join(WORKSPACE, 'memory', 'memory-meta.json');

// ─── Arg Parsing ──────────────────────────────────────────────────────────────

function parseArgs(argv) {
  const args = { query: null, matches: [], dryRun: false };
  let i = 2;
  while (i < argv.length) {
    const arg = argv[i];
    if (arg === '--query' && argv[i + 1]) {
      args.query = argv[++i];
    } else if (arg === '--matches' && argv[i + 1]) {
      args.matches.push(argv[++i]);
    } else if (arg === '--dry-run') {
      args.dryRun = true;
    }
    i++;
  }
  return args;
}

// ─── Hash (must match bootstrap) ─────────────────────────────────────────────

function hashKey(line) {
  return crypto
    .createHash('md5')
    .update(line.substring(0, 20))
    .digest('hex')
    .substring(0, 12);
}

// ─── Fuzzy match helpers ──────────────────────────────────────────────────────

/**
 * Normalise a string for comparison: lowercase, collapse whitespace.
 */
function normalise(s) {
  return s.toLowerCase().replace(/\s+/g, ' ').trim();
}

/**
 * Find the best matching entry for a given recall line.
 * Strategy:
 *   1. Exact hash match on first 20 chars
 *   2. Exact substring match on stored key (first 60 chars)
 *   3. Best fuzzy overlap (word-level Jaccard similarity)
 * Returns { key, entry, score, method } or null.
 */
function findBestMatch(recallLine, entries) {
  const normRecall = normalise(recallLine);

  // 1. Exact hash
  const exactKey = hashKey(recallLine);
  if (entries[exactKey]) {
    return { key: exactKey, entry: entries[exactKey], score: 1.0, method: 'exact-hash' };
  }

  // 2. Substring match on stored key field
  for (const [k, e] of Object.entries(entries)) {
    if (normRecall.includes(normalise(e.key)) || normalise(e.key).includes(normRecall)) {
      return { key: k, entry: e, score: 0.95, method: 'substring' };
    }
  }

  // 3. Jaccard word overlap
  const recallWords = new Set(normRecall.split(/\W+/).filter(Boolean));
  let bestKey = null;
  let bestScore = 0;
  let bestEntry = null;

  for (const [k, e] of Object.entries(entries)) {
    const entryWords = new Set(normalise(e.key).split(/\W+/).filter(Boolean));
    const intersection = [...recallWords].filter((w) => entryWords.has(w)).length;
    const union = new Set([...recallWords, ...entryWords]).size;
    const jaccard = union > 0 ? intersection / union : 0;
    if (jaccard > bestScore) {
      bestScore = jaccard;
      bestKey = k;
      bestEntry = e;
    }
  }

  if (bestScore >= 0.3 && bestKey) {
    return { key: bestKey, entry: bestEntry, score: bestScore, method: 'fuzzy' };
  }

  return null;
}

// ─── Meta I/O ────────────────────────────────────────────────────────────────

function loadMeta() {
  if (!fs.existsSync(META_PATH)) {
    console.warn('⚠️  memory-meta.json not found — creating empty shell.');
    return { schema_version: 1, entries: {} };
  }
  return JSON.parse(fs.readFileSync(META_PATH, 'utf8'));
}

/**
 * Create an on-the-fly entry for an unknown line.
 */
function createOnTheFly(line, now) {
  return {
    key: line.substring(0, 60).trim(),
    created: now,
    lastConfirmed: now,
    lastRecalled: now,
    recallCount: 1,
    tier: 'hot',
    source: 'conversation',
    decayScore: 1.0,
    validFrom: now,
    validUntil: null,
    supersededBy: null,
  };
}

// ─── Main ─────────────────────────────────────────────────────────────────────

function main() {
  const args = parseArgs(process.argv);

  if (!args.query || args.matches.length === 0) {
    console.error('Usage: memory-recall-logger.js --query <text> --matches <line> [--matches <line> ...]');
    process.exit(1);
  }

  const meta = loadMeta();
  const now = new Date().toISOString();
  const updated = [];
  const created = [];

  for (const matchLine of args.matches) {
    const result = findBestMatch(matchLine, meta.entries);

    if (result) {
      const { key, entry, score, method } = result;
      entry.recallCount = (entry.recallCount || 0) + 1;
      entry.lastRecalled = now;
      updated.push({ key, label: entry.key, score: score.toFixed(2), method });
    } else {
      // Create on-the-fly
      const key = hashKey(matchLine);
      meta.entries[key] = createOnTheFly(matchLine, now);
      created.push({ key, label: matchLine.substring(0, 60) });
    }
  }

  // Report
  console.log(`🔍  Query: "${args.query}"`);
  if (updated.length > 0) {
    console.log(`✅  Updated ${updated.length} entry/entries:`);
    for (const u of updated) {
      console.log(`    [${u.method} score=${u.score}] "${u.label}"`);
    }
  }
  if (created.length > 0) {
    console.log(`➕  Created ${created.length} on-the-fly entry/entries:`);
    for (const c of created) {
      console.log(`    "${c.label}"`);
    }
  }

  if (args.dryRun) {
    console.log('🔍  DRY RUN — no files written.');
    return;
  }

  fs.writeFileSync(META_PATH, JSON.stringify(meta, null, 2) + '\n', 'utf8');
  console.log(`💾  memory-meta.json saved.`);
}

main();
