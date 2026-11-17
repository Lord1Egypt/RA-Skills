#!/usr/bin/env node
// Pull a value out of MuseScore's HTML-entity-encoded JSON store.
//
// MuseScore server-renders NO result cards / DOM tables — the data is a JSON
// blob embedded in the markup as HTML-attribute-escaped text (its analogue of
// a Next.js `__NEXT_DATA__` blob). This mirrors musescore-mcp's
// `src/store.ts` (`recoverJson` + `findArrayByKey` / `findEnclosingObject`,
// with mcp-utils `matchBalanced` inlined) and the predicates its parsers apply,
// as a dependency-free script so the fpx skill doesn't need the MCP
// installed. tests/skill-store-parity.test.ts runs both copies on the same
// stores, so a change to one that is not made to the other fails CI.
//
// Usage:
//   node extract-store.mjs <key>                  # the ARRAY that is the value of "<key>":
//   node extract-store.mjs <key> --object         # the enclosing OBJECT that contains "<key>":
//   node extract-store.mjs license --object --id <scoreId>
//                                                 # the main score object for THAT score id
//
// Reads HTML on stdin, writes JSON on stdout.
//
// Examples:
//   fpx get '.../sheetmusic?text=zelda&recording_type=free-download' -p musescore \
//     | node extract-store.mjs scores
//   fpx get '.../user/12345/scores/67890' -p musescore \
//     | node extract-store.mjs type_download_list
//   fpx get '.../user/12345/scores/67890' -p musescore \
//     | node extract-store.mjs license --object --id 67890   # the main score object

import { realpathSync } from 'node:fs';
import { pathToFileURL } from 'node:url';

// Reverse HTML-attribute escaping. Order matters: decode `&amp;` LAST so a
// literal `&quot;` in the data (encoded as `&amp;quot;`) round-trips instead
// of collapsing into a bare quote.
export function recoverJson(s) {
  return s
    .replace(/&quot;/g, '"')
    .replace(/&#0?39;/g, "'")
    .replace(/&#x27;/gi, "'")
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&amp;/g, '&');
}

// mcp-utils/scrape `matchBalanced`, inlined: the EXCLUSIVE end index of the
// `{…}` / `[…]` value starting at `start`, or -1 when `start` is not an opener
// or the structure never closes (or closes with the wrong bracket). Aware of
// both "…" and '…' strings, so quoted brackets don't confuse the depth count.
export function matchBalanced(text, start) {
  const opener = text[start];
  if (opener !== '{' && opener !== '[') return -1;
  const stack = [];
  let inString = null;
  let escape = false;
  for (let i = start; i < text.length; i++) {
    const ch = text[i];
    if (inString) {
      if (escape) escape = false;
      else if (ch === '\\') escape = true;
      else if (ch === inString) inString = null;
      continue;
    }
    if (ch === '"' || ch === "'") {
      inString = ch;
    } else if (ch === '{' || ch === '[') {
      stack.push(ch);
    } else if (ch === '}' || ch === ']') {
      const open = stack.pop();
      if ((ch === '}' && open !== '{') || (ch === ']' && open !== '[')) return -1;
      if (stack.length === 0) return i + 1;
    }
  }
  return -1;
}

// Total bracket-matching work per search, as a multiple of the input length,
// so a hostile store (thousands of nested candidates that all fail) cannot
// make a search quadratic. Mirrors SCAN_BUDGET_FACTOR in src/store.ts.
const SCAN_BUDGET_FACTOR = 8;
const MIN_SCAN_BUDGET = 1 << 16;
const scanBudget = (decoded) => Math.max(SCAN_BUDGET_FACTOR * decoded.length, MIN_SCAN_BUDGET);

// The array that is the value of the first `"<key>":[` in `decoded` — e.g.
// search results live under `"scores"`, distinct from sibling feeds like
// `"see_other_scores"` / `"scores_to_be_promoted"` (none of those contain the
// literal `"scores":`). Skips occurrences whose value isn't a non-empty array
// of predicate-matching objects.
export function findArrayByKey(decoded, key, predicate = () => true) {
  const needle = `"${key}":`;
  let budget = scanBudget(decoded);
  let from = 0;
  for (;;) {
    const at = decoded.indexOf(needle, from);
    if (at < 0) return null;
    from = at + needle.length;
    let p = from;
    while (p < decoded.length && /\s/.test(decoded[p])) p++;
    if (decoded[p] === '[') {
      const end = matchBalanced(decoded, p);
      budget -= (end < 0 ? decoded.length : end) - p;
      if (budget < 0) return null;
      if (end >= 0) {
        try {
          const arr = JSON.parse(decoded.slice(p, end));
          if (Array.isArray(arr) && arr.length > 0 && arr[0] && typeof arr[0] === 'object' && predicate(arr[0])) {
            return arr;
          }
        } catch {
          // not valid JSON here — keep scanning for another match
        }
      }
    }
  }
}

// The innermost JSON object that contains the literal `"<key>":` and also
// satisfies the predicate. One forward brace-stack pass finds each
// occurrence's enclosing `{`; each enclosing object is matched and parsed at
// most once; total work is capped by the scan budget.
export function findEnclosingObject(decoded, key, predicate = () => true) {
  const needle = `"${key}":`;
  let budget = scanBudget(decoded);
  const tried = new Set();
  const open = [];
  let scanned = 0;
  let from = 0;
  for (;;) {
    const i = decoded.indexOf(needle, from);
    if (i < 0) return null;
    for (; scanned < i; scanned++) {
      const c = decoded.charCodeAt(scanned);
      if (c === 0x7b) open.push(scanned);
      else if (c === 0x7d && open.length > 0) open.pop();
    }
    const start = open.length > 0 ? open[open.length - 1] : -1;
    if (start >= 0 && !tried.has(start)) {
      tried.add(start);
      const end = matchBalanced(decoded, start);
      budget -= (end < 0 ? decoded.length : end) - start;
      if (budget < 0) return null;
      if (end >= 0) {
        try {
          const obj = JSON.parse(decoded.slice(start, end));
          if (obj && typeof obj === 'object' && predicate(obj)) return obj;
        } catch {
          // fall through to next occurrence
        }
      }
    }
    from = i + needle.length;
  }
}

// The predicates musescore-mcp's parsers apply for each key it reads, so the
// skill picks the same blob the MCP would. `license --object` takes the main
// score object (the one carrying `is_public_domain`), and with `--id` only the
// one whose `id` is that score — a related score earlier in the store must
// never be reported in its place (its entitlement flags differ).
export function isScoreResult(o) {
  return 'id' in o && 'title' in o && 'is_downloadable' in o;
}
export function isMainScore(o) {
  return 'id' in o && 'is_public_domain' in o;
}
export function predicateFor(key, { object = false, id } = {}) {
  if (!object) return key === 'scores' ? isScoreResult : () => true;
  switch (key) {
    case 'license':
      return (o) => isMainScore(o) && (id === undefined || String(o.id) === String(id));
    case 'measures':
      return (o) => 'keysig' in o;
    case 'type_download_list':
      return (o) => Array.isArray(o.type_download_list);
    default:
      return () => true;
  }
}

/** Run the extraction for parsed CLI args; returns the result or null. */
export function extract(html, key, { object = false, id } = {}) {
  const decoded = recoverJson(html);
  const predicate = predicateFor(key, { object, id });
  return object ? findEnclosingObject(decoded, key, predicate) : findArrayByKey(decoded, key, predicate);
}

function main() {
  const args = process.argv.slice(2);
  const key = args[0];
  const object = args.includes('--object');
  const idAt = args.indexOf('--id');
  const id = idAt >= 0 ? args[idAt + 1] : undefined;
  if (!key || key.startsWith('--') || (idAt >= 0 && !id)) {
    console.error('usage: extract-store.mjs <key> [--object] [--id <scoreId>]');
    process.exit(1);
  }
  let html = '';
  process.stdin.setEncoding('utf8');
  process.stdin.on('data', (chunk) => (html += chunk));
  process.stdin.on('end', () => {
    const result = extract(html, key, { object, ...(id !== undefined ? { id } : {}) });
    if (result === null) {
      console.error(`No ${object ? 'object' : 'array'} found for key "${key}"${id ? ` with id ${id}` : ''}.`);
      process.exit(1);
    }
    process.stdout.write(JSON.stringify(result));
  });
}

const invoked = (() => {
  try {
    return process.argv[1] !== undefined && pathToFileURL(realpathSync(process.argv[1])).href === import.meta.url;
  } catch {
    return false;
  }
})();
if (invoked) main();
