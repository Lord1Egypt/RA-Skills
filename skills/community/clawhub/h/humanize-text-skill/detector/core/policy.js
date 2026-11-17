/**
 * core/policy — auditable strategy loader (language-agnostic).
 *
 * Loads policy/*.toml at module load and exposes the scene×tier×voice strategy
 * as data, not prose. This is humanize-text-skill's upgrade over both parent projects:
 * avoid-ai-writing hardcodes tier thresholds in SKILL.md; shuorenhua describes
 * scene levels in prose. Here they are data — checkable by CI (check-policy.js),
 * adjustable by users, and consumed by the engine.
 *
 * Zero-dependency TOML subset parser (tables, key="value", key=number,
 * key=true/false, arrays). Sufficient for policy/*.toml.
 */
'use strict';

const fs = require('node:fs');
const path = require('node:path');
const REQUIRED_POLICIES = new Set(['scenes.toml', 'tiers.toml', 'matrix.toml', 'voice.toml']);

function parseToml(src) {
  const result = {};
  let current = result;
  for (const raw of src.split(/\r?\n/)) {
    const line = raw.replace(/#.*$/, '').trim();
    if (!line) continue;
    const table = line.match(/^\[([^\]]+)\]$/);
    if (table) {
      const parts = table[1].split('.').map((s) => s.trim());
      current = result;
      for (const p of parts) {
        current[p] = current[p] || {};
        current = current[p];
      }
      continue;
    }
    const kv = line.match(/^([A-Za-z0-9_]+)\s*=\s*(.+)$/);
    if (!kv) continue; // tolerate blank/unparseable
    const [, key, rawVal] = kv;
    const v = rawVal.trim();
    let val;
    if (v === 'true') val = true;
    else if (v === 'false') val = false;
    else if (/^-?\d+(\.\d+)?$/.test(v)) val = Number(v);
    else if (v.startsWith('"')) val = v.replace(/^"|"$/g, '');
    else if (v.startsWith('[')) val = v.slice(1, -1).split(',').map((s) => s.trim().replace(/^"|"$/g, '')).filter(Boolean);
    else val = v;
    current[key] = val;
  }
  return result;
}

function loadPolicy(name) {
  const p = path.join(__dirname, '..', '..', 'policy', name);
  if (!fs.existsSync(p)) {
    if (REQUIRED_POLICIES.has(name)) {
      throw new Error(
        `Missing required policy file: ${p}. ` +
        'Install the full skill package, including the policy/ directory.'
      );
    }
    return {};
  }
  return parseToml(fs.readFileSync(p, 'utf8'));
}

const SCENES = loadPolicy('scenes.toml');
const TIERS = loadPolicy('tiers.toml');
const MATRIX = loadPolicy('matrix.toml');
const VOICE = loadPolicy('voice.toml');

// Resolve the tier action for a given (scene, tier) cell from matrix.toml.
// Returns one of: 'flag' | 'suppress' | 'flag_conservative' | 'flag_relaxed'.
// Falls back to 'flag' (always surface) if undefined — safe default.
function tierAction(scene, tier) {
  const row = MATRIX[scene];
  if (!row) return 'flag';
  return row[tier] || row[`${tier}_action`] || 'flag';
}

// Whether issues of a given tier should be surfaced given the scene.
// 'suppress' hides the tier entirely; the others surface it (the strength
// distinction is consumed by the rewrite level, not the detector).
function shouldSurfaceTier(scene, tier) {
  const action = tierAction(scene, tier);
  return action !== 'suppress';
}

// The default rewrite level for a scene (minimal/standard/aggressive).
function sceneLevel(scene) {
  return (SCENES[scene] && SCENES[scene].level) || 'standard';
}

module.exports = {
  parseToml,
  loadPolicy,
  SCENES,
  TIERS,
  MATRIX,
  VOICE,
  tierAction,
  shouldSurfaceTier,
  sceneLevel,
};
