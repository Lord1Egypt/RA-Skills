#!/usr/bin/env node
/**
 * memory-decay.js
 * Recalculates decay scores for all entries in memory-meta.json
 * and handles tier transitions.
 *
 * Usage:
 *   node scripts/memory-decay.js [--dry-run] [--verbose]
 *
 * Tier maxAgeDays:
 *   hot   → 2 days
 *   warm  → 30 days
 *   cold  → 365 days
 *
 * Formula:
 *   baseDecay    = 1.0 - (daysSinceCreated / maxAgeDays)
 *   recallBoost  = min(recallCount * 0.05, 0.5)
 *   recencyBoost = lastRecalled within 7d? 0.2 : within 30d? 0.1 : 0
 *   decayScore   = clamp(baseDecay + recallBoost + recencyBoost, 0.0, 1.0)
 *
 * Structural entries never decay below 0.3.
 *
 * Tier transitions:
 *   hot  → warm:     after 48h
 *   warm → cold:     after 30d OR decayScore > 0.6 (frequently recalled)
 *   cold → archived: decayScore < 0.1 AND recallCount < 2
 */

'use strict';

const fs = require('fs');
const path = require('path');

const WORKSPACE = path.resolve(__dirname, '..');
const META_PATH = path.join(WORKSPACE, 'memory', 'memory-meta.json');
const DREAM_LOG = path.join(WORKSPACE, 'memory', 'dream-log.md');
const ARCHIVE_DIR = path.join(WORKSPACE, 'memory', 'archive');

const DRY_RUN = process.argv.includes('--dry-run');
const VERBOSE = process.argv.includes('--verbose');

// ─── Constants ────────────────────────────────────────────────────────────────

const MAX_AGE_DAYS = {
  hot: 2,
  warm: 30,
  cold: 365,
};

const STRUCTURAL_FLOOR = 0.3;
const CRYSTALLISE_THRESHOLD = 20; // recallCount to auto-crystallise

// ─── Helpers ─────────────────────────────────────────────────────────────────

function daysSince(isoDate) {
  if (!isoDate) return Infinity;
  return (Date.now() - new Date(isoDate).getTime()) / (1000 * 60 * 60 * 24);
}

function clamp(val, min, max) {
  return Math.min(Math.max(val, min), max);
}

/**
 * Calculate decay score for a single entry.
 */
function calculateDecay(entry, now) {
  const tier = entry.tier || 'cold';

  // Crystallised entries never decay
  if (tier === 'crystallised') return 1.0;

  const maxAgeDays = MAX_AGE_DAYS[tier] || MAX_AGE_DAYS.cold;

  const daysSinceCreated = daysSince(entry.created);
  const baseDecay = 1.0 - daysSinceCreated / maxAgeDays;

  const recallBoost = Math.min((entry.recallCount || 0) * 0.05, 0.5);

  let recencyBoost = 0;
  if (entry.lastRecalled) {
    const daysSinceRecall = daysSince(entry.lastRecalled);
    if (daysSinceRecall <= 7) recencyBoost = 0.2;
    else if (daysSinceRecall <= 30) recencyBoost = 0.1;
  }

  let score = clamp(baseDecay + recallBoost + recencyBoost, 0.0, 1.0);

  // Structural floor
  if (entry.structural && score < STRUCTURAL_FLOOR) {
    score = STRUCTURAL_FLOOR;
  }

  return parseFloat(score.toFixed(4));
}

/**
 * Determine new tier for an entry based on age and decay score.
 * Returns { tier, transition } — transition is a description string or null.
 */
function computeTier(entry, newScore) {
  const current = entry.tier || 'cold';
  const ageHours = daysSince(entry.created) * 24;
  const ageDays = ageHours / 24;
  const recalls = entry.recallCount || 0;

  // Crystallised entries stay crystallised
  if (current === 'crystallised') return { tier: 'crystallised', transition: null };

  // Any tier can crystallise if recall threshold met
  if (recalls >= CRYSTALLISE_THRESHOLD) {
    return { tier: 'crystallised', transition: `${current}→crystallised (recalls=${recalls} ≥${CRYSTALLISE_THRESHOLD})` };
  }

  if (current === 'hot' && ageHours >= 48) {
    return { tier: 'warm', transition: 'hot→warm (age ≥48h)' };
  }

  if (current === 'warm') {
    if (ageDays >= 30) {
      return { tier: 'cold', transition: 'warm→cold (age ≥30d)' };
    }
    if (newScore > 0.6) {
      return { tier: 'cold', transition: `warm→cold (high recall, score=${newScore})` };
    }
  }

  if (current === 'cold') {
    // Don't archive superseded entries — they have historical value via the chain
    if (entry.validUntil) return { tier: current, transition: null };
    if (newScore < 0.1 && recalls < 2) {
      return { tier: 'archived', transition: `cold→archived (score=${newScore}, recalls=${recalls})` };
    }
  }

  return { tier: current, transition: null };
}

// ─── Archive helpers ──────────────────────────────────────────────────────────

function ensureArchiveDir() {
  if (!fs.existsSync(ARCHIVE_DIR)) {
    fs.mkdirSync(ARCHIVE_DIR, { recursive: true });
  }
}

function archiveEntry(entry, key) {
  ensureArchiveDir();
  const now = new Date();
  const monthKey = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
  const archivePath = path.join(ARCHIVE_DIR, `${monthKey}.md`);

  const line =
    `\n<!-- archived: ${now.toISOString()} | key: ${key} | recalls: ${entry.recallCount || 0} | score: ${entry.decayScore} -->\n` +
    `- ${entry.key}\n`;

  fs.appendFileSync(archivePath, line, 'utf8');
}

// ─── Meta I/O ────────────────────────────────────────────────────────────────

function loadMeta() {
  if (!fs.existsSync(META_PATH)) {
    console.warn('⚠️  memory-meta.json not found — nothing to decay.');
    return null;
  }
  return JSON.parse(fs.readFileSync(META_PATH, 'utf8'));
}

function appendDreamLog(message) {
  const ts = new Date().toISOString().split('T')[0];
  const line = `[${ts}] [Memory Decay] ${message}\n`;
  fs.appendFileSync(DREAM_LOG, line, 'utf8');
}

// ─── Main ─────────────────────────────────────────────────────────────────────

function main() {
  const meta = loadMeta();
  if (!meta) process.exit(0);

  const now = new Date().toISOString();
  const entries = meta.entries;
  const totalCount = Object.keys(entries).length;

  let updated = 0;
  let transitions = [];
  let archived = 0;
  const toDelete = [];

  for (const [key, entry] of Object.entries(entries)) {
    const oldScore = entry.decayScore;
    const oldTier = entry.tier;

    const newScore = calculateDecay(entry, now);
    const { tier: newTier, transition } = computeTier(entry, newScore);

    const changed = newScore !== oldScore || newTier !== oldTier;

    if (changed) {
      updated++;
      if (VERBOSE) {
        console.log(`  ${key} "${entry.key.substring(0, 40)}"`);
        console.log(`    score: ${oldScore} → ${newScore} | tier: ${oldTier} → ${newTier}`);
        if (transition) console.log(`    transition: ${transition}`);
      }
    }

    entry.decayScore = newScore;

    if (newTier !== oldTier) {
      entry.tier = newTier;
      transitions.push({ key, from: oldTier, to: newTier, label: entry.key.substring(0, 50) });

      if (newTier === 'archived') {
        if (!DRY_RUN) archiveEntry(entry, key);
        toDelete.push(key);
        archived++;
      }
    }
  }

  // Remove archived entries from live meta
  if (!DRY_RUN) {
    for (const key of toDelete) {
      delete entries[key];
    }
  }

  // Tier counts after update
  const tierCounts = {};
  for (const e of Object.values(entries)) {
    tierCounts[e.tier] = (tierCounts[e.tier] || 0) + 1;
  }

  // Report
  console.log('⚖️   Memory Decay Calculator');
  console.log('────────────────────────────────────────');
  console.log(`  Total entries:     ${totalCount}`);
  console.log(`  Scores updated:    ${updated}`);
  console.log(`  Tier transitions:  ${transitions.length}`);
  console.log(`  Archived:          ${archived}`);
  console.log('\n🏷️   Tier distribution after update:');
  for (const [tier, count] of Object.entries(tierCounts)) {
    console.log(`  ${tier}: ${count}`);
  }

  if (transitions.length > 0) {
    console.log('\n🔄  Tier transitions:');
    for (const t of transitions) {
      console.log(`  [${t.from}→${t.to}] "${t.label}"`);
    }
  }

  if (DRY_RUN) {
    console.log('\n🔍  DRY RUN — no files written.');
    return;
  }

  fs.writeFileSync(META_PATH, JSON.stringify(meta, null, 2) + '\n', 'utf8');
  console.log(`\n💾  memory-meta.json saved.`);

  // Log to dream-log
  const logLine =
    `Ran decay. Entries: ${totalCount}. Updated: ${updated}. ` +
    `Transitions: ${transitions.length}. Archived: ${archived}. ` +
    `Tiers: ${JSON.stringify(tierCounts)}`;
  appendDreamLog(logLine);
}

main();
