/**
 * humanize-text-skill — policy ↔ engine alignment check
 *
 * policy/*.toml is the auditable expression of the scene × tier × voice
 * strategy. This script makes the contract executable by loading the SAME
 * policy module the engine uses (core/policy.js) and asserting:
 *
 *   - policy loads cleanly (valid TOML, all 4 files present)
 *   - matrix.toml covers every scene × tier cell (no gaps)
 *   - the engine enums stay in lockstep with what policy references
 *
 * This is the humanize-text-skill-specific CI guard: the two parent projects hardcode
 * these axes in prose; here they are data, and data gets checked.
 *
 * Dependency-free; runs on node >= 18.
 */
'use strict';

const assert = require('node:assert/strict');
const path = require('node:path');

let failed = 0;
function check(name, fn) {
  try {
    fn();
    console.log(`  \u2713 ${name}`);
  } catch (err) {
    failed++;
    console.error(`  \u2717 ${name}`);
    console.error(`    ${err.message}`);
  }
}

// Engine enums — single source of truth, mirrored here for CI independence.
// If the engine enums move, update both this and the VALID_* sets in patterns.js.
const SCENES = ['chat', 'status', 'docs', 'public-writing'];
const TIERS = ['T1', 'T2', 'T3'];
const VOICES = ['none', 'casual', 'professional', 'technical', 'warm', 'blunt', 'custom'];

console.log('policy \u2194 engine alignment');

// Load the engine's policy module — proves it loads + the TOML parses.
let policy;
check('core/policy.js loads all 4 policy files', () => {
  policy = require(path.join(__dirname, '..', 'detector', 'core', 'policy.js'));
  assert.ok(policy.SCENES && Object.keys(policy.SCENES).length === 4, 'scenes.toml should have 4 scenes');
  assert.ok(policy.TIERS && Object.keys(policy.TIERS).length === 3, 'tiers.toml should have 3 tiers');
  assert.ok(policy.MATRIX && Object.keys(policy.MATRIX).length === 4, 'matrix.toml should have 4 scene rows');
  assert.ok(policy.VOICE && Object.keys(policy.VOICE).length >= 6, 'voice.toml should have >=6 profiles');
});

// scenes.toml references only known scenes, and covers all of them.
check('scenes.toml covers exactly the known scenes', () => {
  const declared = Object.keys(policy.SCENES);
  const unknown = declared.filter((s) => !SCENES.includes(s));
  assert.deepEqual(unknown, [], `scenes.toml declares unknown scenes: ${unknown.join(', ')}`);
  const missing = SCENES.filter((s) => !declared.includes(s));
  assert.deepEqual(missing, [], `scenes.toml missing scenes: ${missing.join(', ')}`);
});

// matrix.toml covers every scene × tier cell — the core anti-drift guard.
check('matrix.toml covers every scene \u00d7 tier cell', () => {
  const missing = [];
  for (const scene of SCENES) {
    const row = policy.MATRIX[scene];
    if (!row) { missing.push(`${scene} (no row)`); continue; }
    for (const tier of TIERS) {
      if (!(tier in row)) missing.push(`${scene}.${tier}`);
    }
  }
  assert.deepEqual(missing, [], `matrix.toml missing cells: ${missing.join(', ')}`);
});

// tiers.toml references only known tiers.
check('tiers.toml references only known tiers', () => {
  const declared = Object.keys(policy.TIERS);
  const unknown = declared.filter((t) => !TIERS.includes(t));
  assert.deepEqual(unknown, [], `tiers.toml declares unknown tiers: ${unknown.join(', ')}`);
});

// voice.toml profiles are all known voices.
check('voice.toml profiles reference only known voices', () => {
  const declared = Object.keys(policy.VOICE);
  const unknown = declared.filter((v) => !VOICES.includes(v));
  assert.deepEqual(unknown, [], `voice.toml declares unknown voices: ${unknown.join(', ')}`);
});

if (failed > 0) {
  console.error(`\n${failed} policy check(s) failed.`);
  process.exit(1);
}
console.log('\npolicy \u2194 engine contract holds.');
