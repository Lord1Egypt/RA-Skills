// Node.js 22+. Uses the public API only; never loads environment files.
export const DEFAULT_BASE = 'https://api.odds-api.net/v1';
export class SkillError extends Error {}

export function baseUrl(value = DEFAULT_BASE) {
  let url;
  try { url = new URL(value); } catch { throw new SkillError('ODDS_API_BASE_URL must be a valid public API URL.'); }
  const official = url.protocol === 'https:' && url.hostname === 'api.odds-api.net' && !url.port;
  const loopback = ['localhost', '127.0.0.1', '[::1]'].includes(url.hostname) && ['http:', 'https:'].includes(url.protocol);
  if ((!official && !loopback) || url.username || url.password || url.search || url.hash || url.pathname.replace(/\/$/, '') !== '/v1') {
    throw new SkillError('Use https://api.odds-api.net/v1 or an explicit loopback /v1 mock server.');
  }
  return url.href.replace(/\/$/, '');
}

function safeRequestId(response) {
  const id = response.headers.get('x-request-id') || '';
  return /^[A-Za-z0-9._:-]{1,128}$/.test(id) ? ` Request ID: ${id}.` : '';
}

export function retryDelay(value, now = Date.now()) {
  if (!value) return null;
  const seconds = Number(value);
  if (Number.isFinite(seconds) && seconds >= 0) return seconds * 1000;
  const date = Date.parse(value);
  return Number.isFinite(date) ? Math.max(0, date - now) : null;
}

export function createClient({
  apiKey = process.env.ODDS_API_KEY,
  base = process.env.ODDS_API_BASE_URL || DEFAULT_BASE,
  fetchImpl = globalThis.fetch,
  sleep = ms => new Promise(resolve => setTimeout(resolve, ms)),
} = {}) {
  const root = baseUrl(base);
  if (typeof apiKey !== 'string' || !apiKey.trim()) throw new SkillError('Set ODDS_API_KEY in your agent runtime. Do not paste it into chat or a command argument.');
  if (/[\r\n]/.test(apiKey)) throw new SkillError('ODDS_API_KEY contains an invalid newline.');
  async function get(path, query = {}) {
    if (!/^\/(sports|leagues|bookmakers|coverage|events(?:\/[A-Za-z0-9._~-]+\/odds\/(?:snapshot|history))?)$/.test(path)) {
      throw new SkillError('Unsupported public read endpoint.');
    }
    const url = new URL(root + path);
    for (const [key, value] of Object.entries(query)) {
      if (/^(?:api_key|apikey|access_token|token|authorization|x-api-key)$/i.test(key)) throw new SkillError('Credentials must be sent only in the authentication header.');
      if (value !== undefined && value !== null && value !== '') url.searchParams.set(key, String(value));
    }
    for (let attempt = 0; attempt < 3; attempt++) {
      let response;
      try {
        response = await fetchImpl(url, {
          headers: { 'X-API-Key': apiKey, Accept: 'application/json' },
          redirect: 'error', signal: AbortSignal.timeout(20000),
        });
      } catch { throw new SkillError('API connection failed or timed out. Check connectivity and retry. Redirects are refused.'); }
      if (response.status === 429) {
        const wait = retryDelay(response.headers.get('retry-after')) ?? 500 * 2 ** attempt + Math.floor(Math.random() * 250);
        if (attempt === 2 || wait > 30000) throw new SkillError(`API rate or quota limit reached. Retry later; check your usage and limits.${safeRequestId(response)}`);
        await response.body?.cancel();
        await sleep(wait);
        continue;
      }
      if (!response.ok) {
        const reason = {
          401: 'Authentication failed. Check your runtime API key.',
          403: 'Access denied. Check the account plan and required add-on or bookmaker access.',
          404: 'Event or resource not found. Discover current IDs before retrying.',
          422: 'The API rejected the filters. Check the current public documentation.',
        }[response.status] || 'The API could not complete the request. Retry later.';
        throw new SkillError(`HTTP ${response.status}: ${reason}${safeRequestId(response)}`);
      }
      let data;
      try { data = await response.json(); } catch { throw new SkillError('The API returned invalid JSON.'); }
      if (!data || typeof data !== 'object' || Array.isArray(data)) throw new SkillError('The API returned an unexpected response shape.');
      return { data, excludedHeader: response.headers.get('x-excluded-bookmakers') || null };
    }
  }
  return { get };
}

export function eventId(value) {
  if (!/^[A-Za-z0-9_-][A-Za-z0-9._~-]{0,199}$/.test(value || '')) throw new SkillError('Supply a canonical --event-id from the events command.');
  return value;
}

export async function collectPages(client, path, query = {}, { snapshot = false, maxPages = 50 } = {}) {
  const pages = [], seen = new Set();
  let cursor;
  let count = 0;
  for (let index = 0; index < maxPages; index++) {
    const page = await client.get(path, { ...query, cursor });
    if (!Array.isArray(page.data.items)) throw new SkillError('Expected an items array from the public endpoint.');
    count += page.data.items.length;
    if (count > 100000) throw new SkillError('Response is too broad. Narrow the event, market, or bookmaker filters.');
    pages.push(page);
    const next = page.data.next_cursor;
    if (snapshot && page.data.complete === false && !next) throw new SkillError('Snapshot is incomplete without a continuation cursor. Narrow filters; no complete comparison can be made.');
    if (snapshot && page.data.complete === true && next) throw new SkillError('Snapshot pagination metadata is inconsistent. Retry the request.');
    if (!next) return pages;
    if (typeof next !== 'string' || seen.has(next)) throw new SkillError('Pagination did not advance. Narrow filters and retry.');
    seen.add(next);
    cursor = next;
  }
  throw new SkillError('Pagination limit reached. Narrow the time window or market filters.');
}

export function utc(value, flag) {
  if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,3})?Z$/.test(value || '')) throw new SkillError(`${flag} must be an ISO 8601 UTC timestamp ending in Z.`);
  const ms = Date.parse(value);
  if (!Number.isFinite(ms) || new Date(ms).toISOString().slice(0, 19) !== value.slice(0, 19)) throw new SkillError(`${flag} is not a valid calendar timestamp.`);
  return ms;
}

export function windowBounds(from, to) {
  const start = utc(from, '--from'), end = utc(to, '--to');
  if (end <= start) throw new SkillError('--to must be later than --from.');
  return { start, end };
}

export function integer(value, fallback, min, max, flag) {
  if (value === undefined) return fallback;
  if (!/^\d+$/.test(String(value)) || Number(value) < min || Number(value) > max) throw new SkillError(`${flag} must be an integer from ${min} to ${max}.`);
  return Number(value);
}

export function parseArgs(argv, allowed) {
  const options = {}, positional = [];
  for (let i = 0; i < argv.length; i++) {
    const part = argv[i];
    if (part === '--help') { options.help = true; continue; }
    if (!part.startsWith('--')) { positional.push(part); continue; }
    const key = part.slice(2);
    if (!allowed.includes(key)) throw new SkillError(`Unsupported option --${/^[a-z-]+$/.test(key) ? key : 'invalid'}. Use --help.`);
    if (Object.hasOwn(options, key)) throw new SkillError(`Duplicate option --${key}.`);
    const value = argv[++i];
    if (value === undefined || value.startsWith('--')) throw new SkillError(`Missing value for --${key}.`);
    options[key] = value;
  }
  if (positional.length > 1) throw new SkillError('Supply one command. Use --help.');
  return { command: positional[0], options };
}

export function assertOptions(options, allowed) {
  for (const key of Object.keys(options)) if (key !== 'help' && !allowed.includes(key)) throw new SkillError(`--${key} does not apply to this command.`);
}

export function stable(value) {
  if (Array.isArray(value)) return value.map(stable);
  if (value && typeof value === 'object') return Object.fromEntries(Object.keys(value).sort().map(key => [key, stable(value[key])]));
  return value ?? null;
}

export function american(decimal) {
  return decimal >= 2 ? `+${Math.round((decimal - 1) * 100)}` : String(Math.round(-100 / (decimal - 1)));
}

export function md(value) { return String(value ?? '').replace(/\|/g, '\\|').replace(/[\r\n]/g, ' '); }
export function csv(value) {
  let text = String(value ?? '');
  // Protect spreadsheet users from formulas in untrusted bookmaker labels.
  if (/^[=+@\-\t\r]/.test(text) && typeof value !== 'number') text = "'" + text;
  return '"' + text.replace(/"/g, '""') + '"';
}

export function fail(error) {
  console.error(error instanceof SkillError ? error.message : 'The skill could not complete the request. Check the input and public documentation.');
  process.exitCode = 1;
}
