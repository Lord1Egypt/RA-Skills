#!/usr/bin/env node
/**
 * memory-bootstrap.js
 * One-time script to seed memory-meta.json from existing MEMORY.md entries.
 *
 * Usage: node scripts/memory-bootstrap.js [--dry-run]
 */

'use strict';

const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const WORKSPACE = path.resolve(__dirname, '..');
const MEMORY_MD = path.join(WORKSPACE, 'MEMORY.md');
const META_PATH = path.join(WORKSPACE, 'memory', 'memory-meta.json');
const BIRTH_DATE = '2026-02-06T00:00:00Z';

const DRY_RUN = process.argv.includes('--dry-run');

// Patterns that indicate a "structural" entry (should never fully decay)
const STRUCTURAL_PATTERNS = [
  // Server IPs / hostnames
  /\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b/,
  // Ports
  /port[:\s]+\d{2,5}/i,
  // API keys / tokens (common shapes)
  /api[_\- ]?key/i,
  /\btoken\b/i,
  /\.env\b/,
  // Config paths
  /\/(srv|etc|var|home|root|opt|usr)\//,
  // Passwords / secrets
  /password/i,
  /secret/i,
  /credential/i,
  // SSH / Docker / server infra keywords
  /\bssh\b/i,
  /\bdocker\b/i,
  /\bpm2\b/i,
  /\bpm2\b/i,
  // People's names (capitalized words that look like names — heuristic)
  /\b[A-Z][a-z]+ [A-Z][a-z]+\b/,
  // Relationships / family
  /\b(wife|husband|daughter|son|sister|brother|mother|father|parent|mum|dad)\b/i,
  // Identity / preferences
  /\bprefer(ence|s)?\b/i,
  /\bpersona\b/i,
  // URLs / domains
  /https?:\/\//,
  /\.(com|co\.uk|io|dev|net|org)\b/i,
  // Known high-value keywords
  /\bstripe\b/i,
  /\btwilio\b/i,
  /\bwebhook\b/i,
  /\bbaselin/i,
  /\bcredential/i,
  /\bcron\b/i,
];

/**
 * Generate a stable hash key from the first 20 chars of a line.
 */
function hashKey(line) {
  return crypto
    .createHash('md5')
    .update(line.substring(0, 20))
    .digest('hex')
    .substring(0, 12);
}

/**
 * Truncate to first 60 chars for human-readable key.
 */
function readableKey(line) {
  return line.substring(0, 60).trim();
}

/**
 * Determine if a line is "structural" based on content heuristics.
 */
function isStructural(line) {
  return STRUCTURAL_PATTERNS.some((re) => re.test(line));
}

/**
 * Load existing meta or return an empty shell.
 */
function loadMeta() {
  if (fs.existsSync(META_PATH)) {
    try {
      return JSON.parse(fs.readFileSync(META_PATH, 'utf8'));
    } catch (e) {
      console.warn('⚠️  Existing memory-meta.json is corrupt — starting fresh.');
    }
  }
  return { schema_version: 1, entries: {} };
}

/**
 * Parse MEMORY.md and return all bullet-point lines.
 * Strips leading "- " / "- **" markers for hash stability.
 */
function parseMemoryLines(mdPath) {
  const raw = fs.readFileSync(mdPath, 'utf8');
  const lines = raw.split('\n');

  const results = [];
  let currentSection = 'General';

  for (const rawLine of lines) {
    // Track section headings
    const sectionMatch = rawLine.match(/^##\s+(.+)/);
    if (sectionMatch) {
      currentSection = sectionMatch[1].trim();
      continue;
    }

    // Only process bullet points
    if (!rawLine.trimStart().startsWith('- ')) continue;

    const trimmed = rawLine.trim();
    results.push({ line: trimmed, section: currentSection });
  }

  return results;
}

// ─── Main ─────────────────────────────────────────────────────────────────────

function main() {
  console.log('🧠  Memory Bootstrap');
  console.log('────────────────────────────────────────');

  if (!fs.existsSync(MEMORY_MD)) {
    console.error(`❌  MEMORY.md not found at ${MEMORY_MD}`);
    process.exit(1);
  }

  // Ensure memory/ directory exists
  const memDir = path.join(WORKSPACE, 'memory');
  if (!fs.existsSync(memDir)) {
    fs.mkdirSync(memDir, { recursive: true });
    console.log('  Created memory/');
  }

  const meta = loadMeta();
  const existingCount = Object.keys(meta.entries).length;

  const bulletLines = parseMemoryLines(MEMORY_MD);
  console.log(`  Found ${bulletLines.length} bullet-point lines in MEMORY.md`);

  let added = 0;
  let skipped = 0;
  let structuralCount = 0;
  const sectionStats = {};

  for (const { line, section } of bulletLines) {
    const key = hashKey(line);
    sectionStats[section] = (sectionStats[section] || 0) + 1;

    if (meta.entries[key]) {
      skipped++;
      continue;
    }

    const structural = isStructural(line);
    if (structural) structuralCount++;

    meta.entries[key] = {
      key: readableKey(line),
      section,
      created: BIRTH_DATE,
      lastConfirmed: BIRTH_DATE,
      lastRecalled: null,
      recallCount: 0,
      tier: 'cold',
      source: 'initial',
      decayScore: 1.0,
      structural: structural || undefined,
      // Temporal validity
      validFrom: null,       // when this fact became true (null = unknown/always)
      validUntil: null,      // when this fact stopped being true (null = still true)
      supersededBy: null,    // hash key of the entry that replaced this one
    };

    // Remove undefined keys (structural: undefined → omit)
    if (!meta.entries[key].structural) {
      delete meta.entries[key].structural;
    }

    added++;
  }

  const totalEntries = Object.keys(meta.entries).length;
  const allStructural = Object.values(meta.entries).filter((e) => e.structural).length;

  console.log('\n📊  Results:');
  console.log(`  Previously in meta:   ${existingCount}`);
  console.log(`  Added this run:       ${added}`);
  console.log(`  Already existed:      ${skipped}`);
  console.log(`  Total entries:        ${totalEntries}`);
  console.log(`  Structural entries:   ${allStructural}`);
  console.log(`  Non-structural:       ${totalEntries - allStructural}`);

  console.log('\n📂  Section breakdown:');
  for (const [sec, count] of Object.entries(sectionStats)) {
    console.log(`  ${sec}: ${count}`);
  }

  console.log('\n🏷️   Tier distribution (all cold — initial seeding):');
  const tierCounts = {};
  for (const e of Object.values(meta.entries)) {
    tierCounts[e.tier] = (tierCounts[e.tier] || 0) + 1;
  }
  for (const [tier, count] of Object.entries(tierCounts)) {
    console.log(`  ${tier}: ${count}`);
  }

  if (DRY_RUN) {
    console.log('\n🔍  DRY RUN — no files written.');
    return;
  }

  fs.writeFileSync(META_PATH, JSON.stringify(meta, null, 2) + '\n', 'utf8');
  console.log(`\n✅  Written to ${META_PATH}`);
}

main();
