'use strict';
/**
 * Ground Truth Provider
 * Parses MODEL_GROUND_TRUTH.md YAML blocks → channel map, cron map, model registry.
 * Single Source of Truth for "what channels exist", "what crons should run", etc.
 *
 * Note: MODEL_GROUND_TRUTH.md is now an INDEX file. Detailed configs are in refs/ground-truth/*.md
 * This parser reads the index file which contains the canonical YAML blocks.
 *
 * Re-reads file only when mtime changes (cached in memory).
 */
const fs = require('fs');
const cfg = require('../lib/config');

let _cache = null;
let _mtime = 0;

function parse() {
  const file = cfg.GROUND_TRUTH_FILE;
  try {
    const st = fs.statSync(file);
    if (st.mtimeMs === _mtime && _cache) return _cache;
    _mtime = st.mtimeMs;
  } catch {
    return _cache || { channels: {}, crons: [], models: [], channelNames: {} };
  }

  const raw = fs.readFileSync(file, 'utf8');

  // ── Parse channel mapping ─────────────────────────────────────────
  const channels = {};      // id → {name, file, type, notion_db}
  const channelNames = {};  // id → "#name"
  const chBlock = extractYamlBlock(raw, 'channels:');
  if (chBlock) {
    const re = /- id:\s*"(\d+)"\s*\n\s*name:\s*"([^"]+)"/g;
    let m;
    while ((m = re.exec(chBlock)) !== null) {
      const id = m[1];
      const name = m[2];
      channels[id] = { name, id };
      channelNames[id] = name;

      // Extract optional fields from the block following this match
      const after = chBlock.slice(m.index + m[0].length, chBlock.indexOf('\n  - id:', m.index + m[0].length));
      const typeM = after.match(/type:\s*(\w+)/);
      if (typeM) channels[id].type = typeM[1];
      const fileM = after.match(/file:\s*"([^"]+)"/);
      if (fileM) channels[id].file = fileM[1];
    }
  }

  // ── Parse cron jobs ───────────────────────────────────────────────
  const crons = [];
  const cronBlock = extractYamlBlock(raw, 'cron_jobs:');
  if (cronBlock) {
    const re = /- id:\s*(\S+)\s*\n\s*name:\s*(.+)/g;
    let m;
    while ((m = re.exec(cronBlock)) !== null) {
      const id = m[1];
      const name = m[2].trim();
      const after = cronBlock.slice(m.index, cronBlock.indexOf('\n  - id:', m.index + 1));
      const modelM = after.match(/model:\s*(.+)/);
      const schedM = after.match(/schedule:\s*"([^"]+)"/);
      const delivM = after.match(/delivery_to:\s*"(\d+)"/);
      crons.push({
        id,
        name,
        model: modelM ? modelM[1].trim() : null,
        schedule: schedM ? schedM[1] : null,
        delivery_to: delivM ? delivM[1] : null,
        delivery_channel_name: delivM ? (channelNames[delivM[1]] || null) : null,
      });
    }
  }

  // ── Parse model registry ──────────────────────────────────────────
  const models = [];
  const modelBlock = extractYamlBlock(raw, 'models:');
  if (modelBlock) {
    const re = /- id:\s*(.+)\s*\n\s*alias:\s*(\S+)/g;
    let m;
    while ((m = re.exec(modelBlock)) !== null) {
      models.push({ id: m[1].trim(), alias: m[2].trim() });
    }
  }

  _cache = { channels, crons, models, channelNames };
  console.log(`[ground-truth] loaded: ${Object.keys(channels).length} channels, ${crons.length} crons, ${models.length} models`);
  return _cache;
}

/**
 * Extract a YAML-ish block starting with `key` inside a ```yaml fenced block.
 */
function extractYamlBlock(text, key) {
  // Find the key inside any ```yaml block
  const blocks = text.match(/```yaml\n([\s\S]*?)```/g) || [];
  for (const block of blocks) {
    const inner = block.replace(/```yaml\n/, '').replace(/```$/, '');
    const idx = inner.indexOf(key);
    if (idx >= 0) {
      return inner.slice(idx);
    }
  }
  return null;
}

// ── Public API (used by other providers) ─────────────────────────────
function getChannelName(id) {
  const gt = parse();
  if (gt.channelNames[id]) return gt.channelNames[id];

  // Fallback to workspace channel files: channels/<id>.md with first markdown heading
  try {
    const path = require('path');
    const file = path.join(cfg.WORKSPACE, 'channels', `${id}.md`);
    if (fs.existsSync(file)) {
      const raw = fs.readFileSync(file, 'utf8');
      const m = raw.match(/^#\s+Channel:\s+(.+)\s+\(/m) || raw.match(/^#\s+(.+)$/m);
      if (m && m[1]) {
        let name = m[1].trim();
        name = name.replace(/\s+—\s+.*$/, '');
        name = name.replace(/\s+\(.+\)$/, '');
        name = name.replace(/\s+Channel\s+Config$/i, '');
        name = name.replace(/\s+Gardening\s+Log$/i, '');
        name = name.replace(/\s+Log$/i, '');
        name = name.trim();
        if (!name.startsWith('#') && /频道|Channel/i.test(name)) return null;
        return name.trim();
      }
    }
  } catch {}

  return null;
}

function getChannelMap() {
  return parse().channels;
}

function getCronGroundTruth() {
  return parse().crons;
}

function getModelRegistry() {
  return parse().models;
}

// ── Model Color Palette ───────────────────────────────────────────────
// Visually distinct colors for dark backgrounds, keyed by model alias.
const MODEL_PALETTE = {
  'opus-4.6':               '#c084fc',  // purple
  'sonnet-4.6':             '#60a5fa',  // blue
  'gemini-3-flash':         '#34d399',  // emerald
  'gemini-3.1-pro':         '#10b981',  // green
  'gemini-3.1-flash-lite':  '#6ee7b7',  // light mint
  'gpt-5.2':                '#f472b6',  // pink
  'gpt-5.3-codex':          '#fb923c',  // orange
  'gpt-5-mini':             '#fbbf24',  // amber
  'gpt-5.3-instant-latest': '#ef4444',  // red
  'gpt-5.4':                '#f97316',  // deep orange
  'kimi-k2.5':              '#22d3ee',  // cyan  (moonshot/kimi-k2.5)
  'doubao-seed-2-0-pro':    '#a78bfa',  // violet
  'qwen-mac':               '#38bdf8',  // sky
  'qwen-spark':             '#818cf8',  // indigo (legacy alias)
  'qwen-spark-35b':         '#818cf8',  // indigo
  'qwen-spark-27b':         '#6366f1',  // darker indigo
};

function _colorHash(str) {
  let h = 0;
  for (let i = 0; i < str.length; i++) h = str.charCodeAt(i) + ((h << 5) - h);
  return `hsl(${Math.abs(h) % 360},65%,62%)`;
}

// Known ledger aliases that don't appear in MODEL_GROUND_TRUTH.md
// but exist in historical ledger.db rows. Map them to the canonical alias color.
const LEDGER_ALIAS_MAP = {
  // qwen-spark-35b variants
  'local-dgx-spark/Qwen3.5-35B-A3B-UD-Q4_K_XL.gguf': 'qwen-spark-35b',
  'local-dgx-spark/Qwen3.5-35B-A3B':                  'qwen-spark-35b',
  'local-dgx-spark/qwen3.5:35b-a3b':                  'qwen-spark-35b',
  // qwen-spark-27b variants
  'local-dgx-spark-27b/Qwen3.5-27B-Claude-4.6-Opus-Reasoning-Distilled.Q5_K_M.gguf': 'qwen-spark-27b',
  // qwen-mac variants
  'local-macbook-pro/qwen3.5:35b-a3b':                 'qwen-mac',
  // ollama-remote (treated as qwen-spark color — same model)
  'ollama-remote/qwen3.5:35b-a3b':                     'qwen-spark',
  // anthropic double-prefix artifact
  'anthropic/anthropic/claude-sonnet-4-6':             'sonnet-4.6',
  // dirty ledger rows: provider="" model="anthropic/..."
  'anthropic/claude-sonnet-4-6':                       'sonnet-4.6',
  'anthropic/claude-opus-4-6':                         'opus-4.6',
  // openai-codex provider
  'openai-codex/gpt-5.4':                              'gpt-5.4',
  'openai-codex/gpt-5.3-codex':                        'gpt-5.3-codex',
  'openai-codex/gpt-5.3-chat-latest':                  'gpt-5.3-instant-latest',
  // moonshot
  'moonshot/kimi-k2.5':                                'kimi-k2.5',
};

function getModelColorMap() {
  const gt = parse();
  const colors = {};

  // 1. Alias → color (for refreshModelOptions / cron selects)
  for (const m of gt.models) {
    colors[m.alias] = MODEL_PALETTE[m.alias] || _colorHash(m.alias);
  }

  // 2. Full model id → same color (for getModelColor(rawModel) in cost/health tabs)
  for (const m of gt.models) {
    if (m.id) {
      const alias = m.alias;
      const color = MODEL_PALETTE[alias] || _colorHash(alias);
      // id format: "provider/model"
      colors[m.id] = color;
      // Also key by model-name-only part (after /)
      const modelPart = m.id.includes('/') ? m.id.split('/').slice(1).join('/') : m.id;
      if (modelPart) colors[modelPart] = color;
    }
  }

  // 3. Historical ledger orphan variants
  for (const [rawKey, aliasRef] of Object.entries(LEDGER_ALIAS_MAP)) {
    const color = MODEL_PALETTE[aliasRef] || _colorHash(aliasRef);
    colors[rawKey] = color;
    // Also key by model part only
    const modelPart = rawKey.includes('/') ? rawKey.split('/').slice(1).join('/') : rawKey;
    if (modelPart) colors[modelPart] = color;
  }

  return colors;
}

// ── HTTP handler ─────────────────────────────────────────────────────
function register(router) {
  const { jsonReply } = require('../lib/http-helpers');

  router.add('GET', '/api/ground-truth', (_req, res) => {
    const gt = parse();
    jsonReply(res, 200, {
      channels: gt.channels,
      crons: gt.crons,
      models: gt.models,
    });
  });

  router.add('GET', '/api/ground-truth/channels', (_req, res) => {
    jsonReply(res, 200, parse().channels);
  });

  router.add('GET', '/api/ground-truth/model-colors', (_req, res) => {
    jsonReply(res, 200, { colors: getModelColorMap() });
  });
}

module.exports = {
  register,
  parse,
  getChannelName,
  getChannelMap,
  getCronGroundTruth,
  getModelRegistry,
  getModelColorMap,
};
