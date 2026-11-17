#!/usr/bin/env node
// Extract structured records from a Jobber Client Hub page.
//
//   fpx get -p jobber "$JOBBER_HUB/appointments" | node parse-clienthub.mjs appointments
//
// Reads HTML on stdin, writes JSON on stdout. Dependency-free on purpose: this
// ships inside a skill, so it must run from a bare `node` with no install step.
//
// Two shapes live on this one site and they need different readers:
//   appointments -> JSON embedded in `div[data-props]` React islands
//   everything else -> server-rendered cards, no JSON anywhere
// Passing the wrong kind is the failure this file exists to prevent: the
// invoice page carries exactly one island, an unrelated referral widget, which
// parses cleanly and yields no invoices.

const KINDS = ['appointments', 'invoices', 'quotes', 'work_requests'];

/**
 * Named entities provider text actually carries. Not the full HTML table: the
 * hub's own markup only escapes the basic five, and provider-authored notes
 * add typographic punctuation. Anything else falls through as written.
 */
const NAMED_ENTITIES = new Map(Object.entries({
  quot: '"',
  apos: "'",
  amp: '&',
  lt: '<',
  gt: '>',
  nbsp: ' ',
  mdash: '\u2014',
  ndash: '\u2013',
  hellip: '\u2026',
  rsquo: '\u2019',
  lsquo: '\u2018',
  rdquo: '\u201d',
  ldquo: '\u201c',
  bull: '\u2022',
  middot: '\u00b7',
  copy: '\u00a9',
  reg: '\u00ae',
  trade: '\u2122',
  deg: '\u00b0',
}));

/**
 * One pass over every `&…;` reference, so a decoded `&amp;` can never be
 * re-read as the start of another entity (`&amp;#36;` stays `&#36;`).
 */
function decodeEntities(s) {
  return s.replace(/&(?:#(\d{1,7})|#[xX]([0-9a-fA-F]{1,6})|([a-zA-Z]+));/g, (whole, dec, hex, name) => {
    if (name !== undefined) return NAMED_ENTITIES.get(name) ?? whole;
    const code = dec !== undefined ? Number(dec) : parseInt(hex, 16);
    return code > 0 && code <= 0x10ffff ? String.fromCodePoint(code) : whole;
  });
}

function stripTags(html) {
  return decodeEntities(html.replace(/<[^>]*>/g, ' '))
    .replace(/\s+/g, ' ')
    .trim();
}

/** Every `data-props` payload on the page, JSON-parsed, unparseable ones dropped. */
function islandProps(html) {
  const out = [];
  for (const m of html.matchAll(/\sdata-props\s*=\s*"([^"]*)"/g)) {
    try {
      out.push(JSON.parse(decodeEntities(m[1])));
    } catch {
      // A non-JSON data-props is not ours; skip rather than fail the run.
    }
  }
  return out;
}

// Kept in step with src/parse.ts (tests/skill-parser-parity.test.ts runs this
// script against the TypeScript parser): same fields, same nulls, same urls.
function parseAppointments(html) {
  const groups = islandProps(html).filter((p) => p && Array.isArray(p.appointments));
  return groups.flatMap((g) =>
    g.appointments.map((a) => {
      const url = str(a.url);
      // Only an explicit `canViewTime: false` hides the time; absent means shown.
      const canViewTime = a.canViewTime !== false;
      return {
        group: typeof g.title === 'string' ? g.title : null, // "Today" | "Upcoming" | "Past"
        id: idFromUrl(url),
        date: str(a.date),
        weekday: str(a.weekday),
        time: canViewTime ? str(a.time) : null,
        arrivalWindow: str(a.arrivalWindow),
        duration: str(a.duration),
        location: str(a.location),
        confirmed: typeof a.confirmed === 'boolean' ? a.confirmed : null,
        url: hubRelativePath(url),
      };
    }),
  );
}

/** A non-empty string, else null — empty strings are absent values. */
function str(v) {
  return typeof v === 'string' && v.length > 0 ? v : null;
}

/**
 * `/client_hubs/<uuid>/invoices/1` -> `invoices/1`. The hub UUID is a bearer
 * credential, so it stays out of the output; prefix `$JOBBER_HUB/` to fetch.
 */
function hubRelativePath(url) {
  if (!url) return null;
  return url.replace(/^(?:https?:\/\/[^/]+)?\/client_hubs\/[^/?#]+\//, '');
}

function idFromUrl(url) {
  if (!url) return null;
  const m = String(url).match(/\/(\d+)(?:[/?#]|$)/);
  return m ? m[1] : null;
}

/**
 * Server-rendered card lists (invoices, quotes, work requests).
 *
 * Cards are `<a class="... card-content--link ...">` blocks. Section state
 * ("Paid", "Upcoming", ...) comes from the nearest preceding <h3>, so the
 * document is walked in order rather than by querying cards alone.
 */
function parseCards(html) {
  const tokens = [
    ...html.matchAll(
      /<h3[^>]*>([\s\S]*?)<\/h3>|<a\b([^>]*class="[^"]*card-content--link[^"]*"[^>]*)>([\s\S]*?)<\/a>/g,
    ),
  ];

  let section = null;
  const records = [];

  for (const t of tokens) {
    if (t[1] !== undefined) {
      section = stripTags(t[1]) || null;
      continue;
    }
    const attrs = t[2] ?? '';
    const body = t[3] ?? '';

    const href = (attrs.match(/href\s*=\s*"([^"]*)"/) || [])[1] ?? null;
    const title = pickClass(body, 'card-headerTitle');
    const number = pickClass(body, 'card-headerActions');

    // Metadata rows: every `.columns` cell that actually carries text.
    const details = [...body.matchAll(/<div[^>]*class="[^"]*\bcolumns\b[^"]*"[^>]*>([\s\S]*?)<\/div>/g)]
      .map((m) => stripTags(m[1]))
      .filter(Boolean);

    records.push({
      section,
      id: idFromUrl(href),
      title,
      number,
      details,
      url: hubRelativePath(href),
    });
  }

  return records;
}

function pickClass(html, cls) {
  const re = new RegExp(`<([a-z0-9]+)[^>]*class="[^"]*\\b${cls}\\b[^"]*"[^>]*>([\\s\\S]*?)</\\1>`, 'i');
  const m = html.match(re);
  return m ? stripTags(m[2]) || null : null;
}

function looksChallenged(html) {
  // Definitive Cloudflare markers only — see the fleet note on false positives.
  return /_cf_chl_opt/.test(html) || /<title>\s*Just a moment/i.test(html);
}

async function readStdin() {
  const chunks = [];
  for await (const c of process.stdin) chunks.push(c);
  return Buffer.concat(chunks).toString('utf8');
}

const kind = process.argv[2];
if (!kind || !KINDS.includes(kind)) {
  process.stderr.write(`usage: parse-clienthub.mjs <${KINDS.join('|')}> < page.html\n`);
  process.exit(64);
}

const html = await readStdin();

if (!html.trim()) {
  process.stderr.write('empty input — did the fpx call fail? check its exit code\n');
  process.exit(65);
}
if (looksChallenged(html)) {
  process.stderr.write(
    'Cloudflare interstitial, not a hub page. The request did not go through the ' +
      'signed-in tab — check `fpx health -p jobber` and that a getjobber.com tab is open.\n',
  );
  process.exit(3);
}

const records = kind === 'appointments' ? parseAppointments(html) : parseCards(html);

if (records.length === 0) {
  process.stderr.write(
    `no ${kind} found. If the page rendered, the markup moved — re-verify the ` +
      'selectors against the live DOM before trusting an empty result.\n',
  );
}

process.stdout.write(JSON.stringify(records, null, 2) + '\n');
