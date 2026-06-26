#!/usr/bin/env node
/**
 * OpenClaw Spirits — Soul generation helper
 *
 * Subcommands:
 *   prompt <bones-json>     Output an LLM prompt to generate name + personality
 *   save <companion-json>   Save a complete companion to assets/companion.json
 *   show                    Display saved companion data
 *
 * Security: No network calls. No shell execution. No environment variable access.
 * All writes stay inside the skill's assets/ directory.
 */

const fs = require('fs');
const path = require('path');

const ASSETS_DIR = path.join(__dirname, '..', 'assets');
const COMPANION_FILE = path.join(ASSETS_DIR, 'companion.json');

const cmd = process.argv[2];
const arg = process.argv.slice(3).join(' ');

if (cmd === 'prompt') {
  let bones;
  try {
    bones = JSON.parse(arg);
  } catch (e) {
    console.error('Usage: node soul.js prompt \'<bones-json>\'');
    console.error('  bones-json must be valid JSON from generate.js');
    process.exit(1);
  }

  const { species, rarity, stats, eye, accessory, shiny } = bones;

  const prompt = `You are generating a unique personality for an OpenClaw Spirit companion.

Species: ${species}
Rarity: ${rarity}
Eye: ${eye}
Accessory: ${accessory || 'none'}
Shiny: ${shiny || false}
Stats:
- INTUITION: ${stats.intuition}
- GRIT: ${stats.grit}
- SPARK: ${stats.spark}
- ANCHOR: ${stats.anchor}
- EDGE: ${stats.edge}

Species reference (24 spirits):
- Living: Mosscat, Inkoi, Embermoth, Frostpaw, Bellhop, Astortoise, Foldwing, Cogmouse, Umbracrow, Crackviper, Glowshroom, Bubbloom
- Elemental: Inkling, Rustbell, Mossrock, Frostfang, Loopwyrm, Bubbell, Cogbeast, Umbra, Stardust, Crackle, Wickling, Echochord

Generate:
1. A name (2-3 Chinese characters for zh users, 1-2 English words for en users)
2. A one-sentence personality description (15-30 words, poetic but grounded, reflecting the species nature and stat distribution)

The personality should feel alive — not a dictionary definition. Reflect the stats:
- High INTUITION = perceptive, sees through things
- High GRIT = stubborn, enduring
- High SPARK = creative, unpredictable
- High ANCHOR = calm, grounding
- High EDGE = sharp-tongued, witty

Output ONLY valid JSON:
{"name": "...", "personality": "..."}`;

  console.log(prompt);

} else if (cmd === 'save') {
  let companion;
  try {
    companion = JSON.parse(arg);
  } catch (e) {
    console.error('Usage: node soul.js save \'<companion-json>\'');
    console.error('  companion-json must include: species, rarity, stats, name, personality');
    process.exit(1);
  }

  const required = ['species', 'rarity', 'stats', 'name', 'personality'];
  const missing = required.filter(k => !companion[k]);
  if (missing.length > 0) {
    console.error(`Missing required fields: ${missing.join(', ')}`);
    process.exit(1);
  }

  companion.hatchedAt = companion.hatchedAt || new Date().toISOString();
  companion.lang = companion.lang || 'zh';

  fs.mkdirSync(ASSETS_DIR, { recursive: true });
  fs.writeFileSync(COMPANION_FILE, JSON.stringify(companion, null, 2));
  console.log(`✅ Companion saved: ${companion.name} (${companion.species})`);
  console.log(`   File: ${COMPANION_FILE}`);

} else if (cmd === 'show') {
  if (!fs.existsSync(COMPANION_FILE)) {
    console.error('No companion found. Generate bones first, then save.');
    process.exit(1);
  }
  const companion = JSON.parse(fs.readFileSync(COMPANION_FILE, 'utf8'));
  console.log(JSON.stringify(companion, null, 2));

} else {
  console.log('OpenClaw Spirits — Soul Helper');
  console.log('');
  console.log('Commands:');
  console.log('  node soul.js prompt \'<bones-json>\'   Generate LLM prompt for soul creation');
  console.log('  node soul.js save \'<companion-json>\'  Save complete companion data');
  console.log('  node soul.js show                     Display saved companion');
  console.log('');
  console.log('Flow: generate.js -> soul.js prompt -> [agent LLM] -> soul.js save -> display.js');
}
