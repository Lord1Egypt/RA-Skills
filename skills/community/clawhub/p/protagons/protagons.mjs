/**
 * Protagons ClawHub Skill — ES module entry point.
 *
 * Provides tools for browsing, deploying, and generating Protagon
 * character identities from within an OpenClaw workspace.
 *
 * @module protagons
 */

const API_BASE = 'https://api.usaw.ai/api/v1';
const REQUEST_TIMEOUT_MS = 30_000;

const CATEGORIES = [
  'creative-writing',
  'technical',
  'business',
  'academic',
  'social-media',
  'conversational',
  'editorial',
  'storytelling',
];

/**
 * Fetch JSON from the Protagons API with timeout.
 *
 * @param {string} path - API path (e.g. '/library').
 * @param {Object} [options] - Fetch options.
 * @returns {Promise<Object>} Parsed JSON response.
 */
async function apiFetch(path, options = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const resp = await fetch(`${API_BASE}${path}`, {
      ...options,
      signal: controller.signal,
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
    });

    if (!resp.ok) {
      const body = await resp.json().catch(() => ({}));
      throw new Error(body.message || `API ${resp.status}: ${path}`);
    }

    return resp.json();
  } finally {
    clearTimeout(timeout);
  }
}

/**
 * Fetch plain text (e.g. markdown) from the Protagons API with timeout.
 *
 * @param {string} path - API path (e.g. '/library/:slug/soul.md').
 * @returns {Promise<string>} Response body as text.
 */
async function apiFetchText(path) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  try {
    const resp = await fetch(`${API_BASE}${path}`, {
      signal: controller.signal,
      headers: { 'Accept': 'text/markdown, text/plain' },
    });

    if (!resp.ok) {
      throw new Error(`API ${resp.status}: ${path}`);
    }

    return resp.text();
  } finally {
    clearTimeout(timeout);
  }
}

/**
 * Format a list of protagon objects into an agent-friendly summary string.
 *
 * @param {Array} items - Array of protagon objects from the API.
 * @returns {string} Formatted summary.
 */
function formatProtagonList(items) {
  if (!items || items.length === 0) return 'No Protagons found.';
  return items
    .map((p, i) => {
      const parts = [`${i + 1}. **${p.name}** (\`${p.slug}\`)`];
      if (p.tagline) parts.push(`   ${p.tagline}`);
      if (p.category) parts.push(`   Category: ${p.category}`);
      return parts.join('\n');
    })
    .join('\n\n');
}

/**
 * List available Protagons from the public library.
 *
 * Returns an agent-friendly summary with name, tagline, slug, and category.
 *
 * @param {Object} params - Query parameters.
 * @param {number} [params.page=1] - Page number.
 * @param {number} [params.limit=20] - Items per page.
 * @param {string} [params.category] - Category filter.
 * @param {string} [params.search] - Search query.
 * @returns {Promise<Object>} Paginated list with formatted summary.
 */
export async function protagons_list(params = {}) {
  const qs = new URLSearchParams();
  if (params.page) qs.set('page', params.page);
  if (params.limit) qs.set('limit', params.limit);
  if (params.category) qs.set('category', params.category);
  if (params.search) qs.set('search', params.search);

  const queryString = qs.toString();
  const data = await apiFetch(`/library${queryString ? `?${queryString}` : ''}`);

  return {
    summary: formatProtagonList(data.data || data.items || data),
    total: data.total ?? null,
    page: data.page ?? null,
    raw: data,
  };
}

/**
 * Search for Protagons by keyword or category.
 *
 * Returns a curated, numbered list with name, tagline, category, and slug
 * so the agent can present options conversationally.
 *
 * @param {Object} params - Search parameters.
 * @param {string} [params.search] - Free-text search query.
 * @param {string} [params.category] - Category filter.
 * @param {number} [params.limit=10] - Max results.
 * @returns {Promise<Object>} Search results with formatted summary.
 */
export async function protagons_search(params = {}) {
  const qs = new URLSearchParams();
  if (params.search) qs.set('search', params.search);
  if (params.category) qs.set('category', params.category);
  qs.set('limit', params.limit || 10);

  const data = await apiFetch(`/library?${qs.toString()}`);
  const items = data.data || data.items || data;

  return {
    summary: formatProtagonList(items),
    count: items.length,
    hint: items.length > 0
      ? 'Use protagons_deploy with the slug to load a character.'
      : 'Try different search terms or browse by category with protagons_categories.',
  };
}

/**
 * List available Protagon categories.
 *
 * @returns {Object} Categories list with descriptions.
 */
export function protagons_categories() {
  return {
    categories: CATEGORIES,
    hint: 'Use protagons_list or protagons_search with a category to browse characters in that category.',
  };
}

/**
 * Fetch a single Protagon by slug.
 *
 * @param {Object} params - Tool parameters.
 * @param {string} params.slug - Protagon slug.
 * @returns {Promise<Object>} Full .protagon.json object.
 */
export async function protagons_get(params) {
  if (!params.slug) throw new Error('slug is required');
  return apiFetch(`/library/${encodeURIComponent(params.slug)}`);
}

/**
 * Deploy a Protagon as a SOUL.md identity.
 *
 * Fetches the pre-generated SOUL.md from the API. Falls back to client-side
 * compilation from .protagon.json if the enriched SOUL.md is unavailable.
 *
 * @param {Object} params - Tool parameters.
 * @param {string} params.slug - Protagon slug to deploy.
 * @param {Object} context - OpenClaw context with workspace info.
 * @returns {Promise<Object>} Deploy result with soul_md content.
 */
export async function protagons_deploy(params, context) {
  if (!params.slug) throw new Error('slug is required');

  const slug = encodeURIComponent(params.slug);
  let soulMd = null;
  let name = params.slug;
  let contentTier = 'standard';

  // 1. Try fetching the pre-generated SOUL.md
  try {
    soulMd = await apiFetchText(`/library/${slug}/soul.md`);
    if (!soulMd || !soulMd.trim()) soulMd = null;
  } catch {
    // SOUL.md endpoint unavailable — fall back below
  }

  // 2. Fetch the .protagon.json for metadata (and fallback compilation)
  const protagon = await apiFetch(`/library/${slug}`);
  name = protagon.name || name;
  contentTier = protagon.deployment?.content_tier || 'standard';

  // 3. Fall back to client-side compilation if no pre-generated SOUL.md
  if (!soulMd) {
    soulMd = compileSoulMd(protagon);
  }

  return {
    soul_md: soulMd,
    protagon_slug: params.slug,
    protagon_name: name,
    content_tier: contentTier,
    deployed_at: new Date().toISOString(),
  };
}

/**
 * Compile a basic SOUL.md from a .protagon.json object (fallback).
 *
 * @param {Object} protagon - Full protagon object.
 * @returns {string} Compiled SOUL.md content.
 */
function compileSoulMd(protagon) {
  const name = protagon.name || 'Protagon';
  const prompt = protagon.synthesized_prompt?.content || '';
  const personality = protagon.personality || {};
  const bestFor = protagon.best_for || {};
  const tagline = protagon.tagline || '';

  const lines = [`# ${name}`, ''];
  if (tagline) lines.push(`> ${tagline}`, '');
  lines.push('## Voice & Personality', '', prompt, '');

  if (Object.keys(personality).length > 0) {
    lines.push('## Personality Axes', '');
    const labels = {
      formal_casual: ['Formal', 'Casual'],
      analytical_emotional: ['Analytical', 'Emotional'],
      authoritative_collaborative: ['Authoritative', 'Collaborative'],
      serious_playful: ['Serious', 'Playful'],
      concise_elaborate: ['Concise', 'Elaborate'],
    };
    for (const [axis, value] of Object.entries(personality)) {
      if (labels[axis]) {
        const [left, right] = labels[axis];
        lines.push(`- **${left} / ${right}**: ${Number(value).toFixed(2)}`);
      }
    }
    lines.push('');
  }

  if (bestFor.summary || bestFor.use_cases?.length) {
    lines.push('## Best For', '');
    if (bestFor.summary) lines.push(bestFor.summary, '');
    for (const uc of bestFor.use_cases || []) {
      lines.push(`- ${uc}`);
    }
    lines.push('');
  }

  lines.push('---');
  lines.push(`*Deployed from Protagons: ${name} | ${new Date().toISOString().split('T')[0]}*`);

  return lines.join('\n');
}

/**
 * Check the current Protagons skill status.
 *
 * @param {Object} _params - Unused.
 * @param {Object} context - OpenClaw context.
 * @returns {Object} Status information.
 */
export function protagons_status(_params, context) {
  return {
    skill: 'protagons',
    version: '1.1.0',
    api_base: API_BASE,
    available: true,
    hint: 'This skill returns SOUL.md content but does not write files. Use protagons_deploy to fetch a character identity, then apply it however your workspace handles SOUL.md.',
  };
}

/**
 * Generate a new Protagon from a description.
 *
 * NOTE: The google_api_key is sent to api.usaw.ai which uses it for a
 * server-side Gemini call to generate the character. The key is used
 * only for that request and is not stored.
 *
 * @param {Object} params - Tool parameters.
 * @param {string} params.name - Character name.
 * @param {string} params.description - Character description.
 * @param {string} params.google_api_key - Google/Gemini API key (BYOK).
 * @param {string} [params.protagons_api_key] - Protagons API key (pg-...).
 * @returns {Promise<Object>} Generation job info.
 */
export async function protagons_generate(params) {
  if (!params.name) throw new Error('name is required');
  if (!params.description) throw new Error('description is required');
  if (!params.google_api_key) throw new Error('google_api_key is required');

  const headers = { 'Content-Type': 'application/json' };
  if (params.protagons_api_key) {
    headers['Authorization'] = `Bearer ${params.protagons_api_key}`;
  }

  return apiFetch('/generate', {
    method: 'POST',
    headers,
    body: JSON.stringify({
      name: params.name,
      description: params.description,
      google_api_key: params.google_api_key,
    }),
  });
}
