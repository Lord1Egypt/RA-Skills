/**
 * Prompt Template Data Source: awesome-chatgpt-prompts (via jsDelivr CDN)
 *
 * Loads the canonical `prompts.csv` from
 *   https://github.com/f/awesome-chatgpt-prompts
 * and exposes a keyword search over real prompt templates.
 *
 * The same CSV powers https://prompts.chat — so users get the exact
 * prompt strings they'd see on that site, no web scraping required.
 */
const axios = require('axios');

const CSV_URL = 'https://cdn.jsdelivr.net/gh/f/awesome-chatgpt-prompts@main/prompts.csv';
const CACHE_TTL_MS = 6 * 60 * 60 * 1000; // 6 hours

// In-memory cache so repeated calls don't re-download the ~5 MB CSV.
let _cache = { at: 0, rows: null };

// Coarse category buckets, matched against the `act` (role) column.
const CATEGORIES = {
  development: [
    'coding', 'code', 'programming', 'developer', 'software', 'debug',
    'engineer', 'devops', 'react', 'python', 'java', 'sql', 'api',
    'terminal', 'linux', 'git', 'stackoverflow', 'regex',
  ],
  marketing: [
    'marketing', 'social media', 'seo', 'advertis', 'copywrit',
    'brand', 'growth', 'ad ', 'influencer',
  ],
  education: [
    'teacher', 'tutor', 'learn', 'education', 'student', 'academic',
    'professor', 'instructor', 'explain', 'coach', 'mentor',
  ],
  writing: [
    'writ', 'blog', 'essay', 'story', 'content', 'author',
    'novelist', 'poet', 'journalist', 'screenwriter', 'editor',
  ],
  business: [
    'business', 'startup', 'strategy', 'management', 'consult',
    'finance', 'ceo', 'entrepreneur', 'investor', 'recruiter',
  ],
  design: [
    'design', 'ui', 'ux', 'graphic', 'creativ', 'visual',
    'artist', 'illustrat', 'architect',
  ],
  productivity: [
    'productivity', 'workflow', 'automation', 'planning',
    'organization', 'project manager', 'assistant',
  ],
  language: [
    'translator', 'language', 'grammar', 'english', 'communic',
    'linguist', 'interpret', 'pronunciation',
  ],
};

/**
 * Minimal RFC-4180 CSV parser.
 * Handles double-quoted fields, escaped `""`, and embedded newlines.
 */
function parseCSV(text) {
  const rows = [];
  let field = '';
  let row = [];
  let inQuotes = false;

  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (inQuotes) {
      if (c === '"') {
        if (text[i + 1] === '"') {
          field += '"';
          i++;
        } else {
          inQuotes = false;
        }
      } else {
        field += c;
      }
      continue;
    }
    if (c === '"') {
      inQuotes = true;
    } else if (c === ',') {
      row.push(field);
      field = '';
    } else if (c === '\n') {
      row.push(field);
      rows.push(row);
      row = [];
      field = '';
    } else if (c === '\r') {
      // skip; handled with \n
    } else {
      field += c;
    }
  }
  if (field.length || row.length) {
    row.push(field);
    rows.push(row);
  }
  return rows;
}

/**
 * Fetch and parse the prompts CSV (cached for CACHE_TTL_MS).
 * @returns {Promise<Array<{act, prompt, for_devs, type, contributor}>>}
 */
async function loadPrompts() {
  if (_cache.rows && Date.now() - _cache.at < CACHE_TTL_MS) {
    return _cache.rows;
  }

  const { data } = await axios.get(CSV_URL, {
    timeout: 20000,
    responseType: 'text',
    transformResponse: [(v) => v], // keep as raw string
    headers: {
      'User-Agent': 'PromptFinder-OpenClaw-Skill/1.0',
      'Accept': 'text/csv,text/plain',
    },
  });

  const parsed = parseCSV(String(data));
  const header = parsed.shift() || [];
  const idx = {
    act: header.indexOf('act'),
    prompt: header.indexOf('prompt'),
    for_devs: header.indexOf('for_devs'),
    type: header.indexOf('type'),
    contributor: header.indexOf('contributor'),
  };

  if (idx.act < 0 || idx.prompt < 0) {
    throw new Error('Unexpected CSV schema (missing act/prompt columns)');
  }

  const rows = parsed
    .filter((r) => r && r[idx.act] && r[idx.prompt])
    .map((r) => ({
      act: (r[idx.act] || '').trim(),
      prompt: (r[idx.prompt] || '').trim(),
      for_devs: (r[idx.for_devs] || '').toUpperCase() === 'TRUE',
      type: (r[idx.type] || 'TEXT').trim(),
      contributor: (r[idx.contributor] || '').trim(),
    }));

  _cache = { at: Date.now(), rows };
  return rows;
}

/**
 * Auto-categorize a prompt based on its `act` (role) label.
 */
function categorize(act) {
  const lower = (act || '').toLowerCase();
  for (const [cat, kws] of Object.entries(CATEGORIES)) {
    if (kws.some((kw) => lower.includes(kw))) return cat;
  }
  return 'general';
}

/**
 * Check whether a row matches a requested category filter.
 */
function matchesCategory(row, category) {
  const cat = (category || '').toLowerCase().trim();
  if (!cat) return true;

  const text = `${row.act} ${row.type}`.toLowerCase();
  const kws = CATEGORIES[cat] || [cat];
  return kws.some((kw) => text.includes(kw));
}

/**
 * Build a stable slug for the prompts.chat URL fragment.
 */
function slugify(s) {
  return (s || '')
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, '-')
    .replace(/(^-|-$)/g, '');
}

/**
 * Search prompts by keyword with simple relevance scoring.
 *
 * Scoring:
 *   +30  full phrase appears in `act`
 *   +10  any term appears in `act`
 *   + 1  any term appears in `prompt` body
 *
 * @param {string} query
 * @param {string|null} category
 * @param {number} limit  1..20
 * @returns {Promise<Array>} Formatted result objects
 */
async function searchPrompts(query, category = null, limit = 5) {
  limit = Math.min(Math.max(1, parseInt(limit, 10) || 5), 20);

  const q = String(query || '').toLowerCase().trim();
  const terms = q.split(/\s+/).filter(Boolean);
  if (!terms.length) return [];

  const rows = await loadPrompts();
  const scored = [];

  for (const row of rows) {
    if (!matchesCategory(row, category)) continue;

    const actLower = row.act.toLowerCase();
    const promptLower = row.prompt.toLowerCase();
    let score = 0;

    if (actLower.includes(q)) score += 30;
    for (const t of terms) {
      if (actLower.includes(t)) score += 10;
      if (promptLower.includes(t)) score += 1;
    }

    if (score > 0) scored.push({ row, score });
  }

  scored.sort((a, b) => b.score - a.score);

  return scored.slice(0, limit).map(({ row }) => ({
    title: row.act,
    description:
      row.prompt.length > 220
        ? row.prompt.slice(0, 220).trim() + '…'
        : row.prompt,
    prompt: row.prompt,
    category: categorize(row.act),
    url: `https://prompts.chat/#${slugify(row.act)}`,
    source: 'awesome-chatgpt-prompts',
    ...(row.contributor && { author: row.contributor }),
    for_devs: row.for_devs,
    type: row.type,
  }));
}

/**
 * Fetch a single prompt template by exact or partial `act` name.
 */
async function getPromptDetail(title) {
  const rows = await loadPrompts();
  const needle = String(title || '').toLowerCase().trim();
  const found =
    rows.find((r) => r.act.toLowerCase() === needle) ||
    rows.find((r) => r.act.toLowerCase().includes(needle));

  if (!found) {
    throw new Error(`No prompt found for: ${title}`);
  }

  return {
    title: found.act,
    prompt: found.prompt,
    category: categorize(found.act),
    url: `https://prompts.chat/#${slugify(found.act)}`,
    source: 'awesome-chatgpt-prompts',
    contributor: found.contributor || null,
    for_devs: found.for_devs,
    type: found.type,
  };
}

module.exports = {
  searchPrompts,
  getPromptDetail,
  loadPrompts,
  parseCSV,
  CATEGORIES,
};
