import { DEFAULT_PROFILE } from './domains.js';

const PRE_REPLACEMENTS = [
  [/ダンボー?|だんぼう?|だんぼ/g, '暖房'],
  [/じょしつ|ジョシツ/g, '除湿'],
  [/そうふう|ソーフー?|そうふ/g, '送風'],
  [/えあこん|エアコン/g, 'エアコン'],
  [/えあこんとめて|エアコントメテ|エアコンとめて|エアコン止めて|エアコンめて/g, 'エアコン消して'],
  [/いや、?コントめて|イヤ、?コントめて|であかんとめて/g, 'エアコン消して'],
  [/いや、?コント|イヤ、?コント|エヤコント|エアコント|であかん/g, 'エアコン'],
  [/ダンボーツケティ|ダンボーツケテ|だんぼーつけて|だんぼつけて/g, '暖房つけて'],
  [/と、?ボー?ス?けて|とぼーすけて|と、ボースけて/g, '暖房つけて'],
  [/そうしてつけて/g, '除湿つけて'],
  [/Bボールつけて|bボールつけて|びーぼーるつけて/g, '冷房つけて'],
  [/Pをつけて|ピーをつけて|ぴーをつけて/g, '冷房つけて'],
  [/電気化して/g, '電気消して'],
  [/すずしくして|涼しくして/g, '冷房にして'],
  [/あたたかくして|暖かくして/g, '暖房にして'],
];

function compactText(text) {
  return String(text || '').trim().replace(/\s+/g, '');
}

function levenshtein(a, b) {
  const s = String(a || '');
  const t = String(b || '');
  const rows = s.length + 1;
  const cols = t.length + 1;
  const dp = Array.from({ length: rows }, () => Array(cols).fill(0));
  for (let i = 0; i < rows; i += 1) dp[i][0] = i;
  for (let j = 0; j < cols; j += 1) dp[0][j] = j;
  for (let i = 1; i < rows; i += 1) {
    for (let j = 1; j < cols; j += 1) {
      const cost = s[i - 1] === t[j - 1] ? 0 : 1;
      dp[i][j] = Math.min(dp[i - 1][j] + 1, dp[i][j - 1] + 1, dp[i - 1][j - 1] + cost);
    }
  }
  return dp[s.length][t.length];
}

function similarity(a, b) {
  const left = compactText(a);
  const right = compactText(b);
  if (!left || !right) return 0;
  if (left === right) return 1;
  const maxLen = Math.max(left.length, right.length);
  return Math.max(0, 1 - levenshtein(left, right) / maxLen);
}

function normalizeCoolingSurface(text) {
  return String(text || '')
    .replace(/(れいぼう?|れいぼー?|れいほう?|れーほー?|レイボー?|レーボー?|れーぼー?|れいぼ|れーぼ|レイブ|れいぶ|りぃぽ|りーぽ|れぃぽ|リーボー?|リボール?)(ド)?/g, '冷房')
    .replace(/リーボード/g, '冷房')
    .replace(/Liibo|liibo|Riibo|riibo/gi, '冷房')
    .replace(/Tskete|tskete/gi, 'つけて');
}

function normalizeText(input) {
  let text = compactText(input);
  for (const [pattern, value] of PRE_REPLACEMENTS) text = text.replace(pattern, value);
  text = normalizeCoolingSurface(text);
  return text;
}

function findBestAlias(text, aliasMap, threshold = 0.74) {
  const normalized = normalizeText(text);
  let best = null;

  for (const [value, aliases] of Object.entries(aliasMap || {})) {
    for (const alias of aliases) {
      const normalizedAlias = normalizeText(alias);
      let score = 0;
      let matchedBy = 'fuzzy';
      if (normalized.includes(normalizedAlias)) {
        score = normalized === normalizedAlias ? 1 : Math.max(0.84, normalizedAlias.length / normalized.length);
        matchedBy = 'alias';
      } else {
        score = similarity(normalized, normalizedAlias);
      }
      if (!best || score > best.score) {
        best = { value, alias, score, matchedBy };
      }
    }
  }

  if (!best || best.score < threshold) return null;
  return best;
}

function inferDevice(text, profile = DEFAULT_PROFILE) {
  return findBestAlias(text, profile.devices, 0.74);
}

function inferMode(text, profile = DEFAULT_PROFILE) {
  return findBestAlias(text, profile.modes, 0.72);
}

function inferAction(text, profile = DEFAULT_PROFILE) {
  const normalized = normalizeText(text);
  if (/(つけて|つける|オン)/.test(normalized)) return { value: 'on', alias: 'つけて', score: 0.96, matchedBy: 'rule' };
  if (/(消して|けして|オフ|止めて|とめて)/.test(normalized)) return { value: 'off', alias: '消して', score: 0.96, matchedBy: 'rule' };
  if (/(にして|して)/.test(normalized)) return { value: 'set_mode', alias: 'にして', score: 0.94, matchedBy: 'rule' };
  return findBestAlias(text, profile.actions, 0.72);
}

function deriveIntent(slots) {
  if (slots.device === 'light' && slots.action === 'on') return { intent: 'light_on', reason: 'matched light on' };
  if (slots.device === 'light' && slots.action === 'off') return { intent: 'light_off', reason: 'matched light off' };
  if (slots.device === 'aircon' && slots.action === 'on' && !slots.mode) return { intent: 'aircon_on', reason: 'matched aircon on' };
  if (slots.device === 'aircon' && slots.action === 'off' && !slots.mode) return { intent: 'aircon_off', reason: 'matched aircon off' };
  if (slots.device === 'aircon' && slots.mode) return { intent: `aircon_mode_${slots.mode}`, reason: `matched aircon mode ${slots.mode}` };
  if (slots.device === 'curtain' && slots.action === 'open') return { intent: 'curtain_open', reason: 'matched curtain open' };
  if (slots.device === 'curtain' && slots.action === 'close') return { intent: 'curtain_close', reason: 'matched curtain close' };
  if (slots.device === 'tv' && slots.action === 'on') return { intent: 'tv_on', reason: 'matched tv on' };
  if (slots.device === 'tv' && slots.action === 'off') return { intent: 'tv_off', reason: 'matched tv off' };
  return { intent: null, reason: 'no strong match' };
}

function classify(text, profile = DEFAULT_PROFILE) {
  const rawText = String(text || '');
  const normalizedText = normalizeText(rawText);
  const device = inferDevice(normalizedText, profile);
  const mode = inferMode(normalizedText, profile);
  let action = inferAction(normalizedText, profile);
  const candidates = [];

  if (device) candidates.push({ slot: 'device', ...device });
  if (mode) candidates.push({ slot: 'mode', ...mode });
  if (action) candidates.push({ slot: 'action', ...action });

  const slots = {
    device: device?.value || (mode ? 'aircon' : null),
    action: action?.value || null,
    mode: mode?.value || null,
    value: null,
  };

  if (mode) slots.action = 'set_mode';
  if (!action && mode) action = { value: 'set_mode', alias: mode.alias, score: mode.score, matchedBy: 'derived' };

  const { intent, reason } = deriveIntent(slots);
  const scores = [device?.score, mode?.score, action?.score].filter((x) => typeof x === 'number');
  let confidence = scores.length ? Math.min(...scores) : 0;

  if (mode && /(涼しくして|暖かくして|冷房にして|暖房にして)/.test(normalizedText)) {
    confidence = Math.max(confidence, 0.9);
  }

  const needsConfirmation = !intent || confidence < 0.78 || (!device && !mode);

  return {
    rawText,
    normalizedText,
    intent,
    confidence,
    needsConfirmation,
    reason,
    slots,
    candidates,
  };
}

export { PRE_REPLACEMENTS, DEFAULT_PROFILE, normalizeText, findBestAlias, inferDevice, inferMode, inferAction, deriveIntent, classify };
