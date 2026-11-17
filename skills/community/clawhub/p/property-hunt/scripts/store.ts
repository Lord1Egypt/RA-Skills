// The store. `data.js` is the single source of truth AND the file the frontend
// loads — a file:// page cannot fetch(), so anything else would need a derived
// export that can silently go stale. This module is its only writer.
import * as fs from 'node:fs';
import * as path from 'node:path';

/** Scraped from a listing. Replaced wholesale on every re-scrape. */
export type Scraped = {
  address: string;
  city: string;
  state: string;
  zip: string;
  lat: number | null;
  lng: number | null;
  price: number | null;
  beds: number | null;
  baths: number | null;
  sqft: number | null;
  property_type: string | null;
  listing_status: string | null;
  listing_url: string;
  listing_source: string;
  photo: string | null;
  last_scraped_at: string;
};

/** The user's own judgments. A re-scrape must never touch these. */
export type Mine = {
  rating: number | null;
  status: string;
  notes: string;
  added_at: string;
};

export type Property = { id: string; scraped: Scraped; mine: Mine };

export const MINE_FIELDS = ['rating', 'status', 'notes'] as const;

const HEADER = 'window.PROPERTIES =';

// Street-type abbreviations, so "424 28th Street" and "424 28th St" are one house.
const SUFFIXES: Record<string, string> = {
  street: 'st',
  avenue: 'ave',
  road: 'rd',
  drive: 'dr',
  boulevard: 'blvd',
  lane: 'ln',
  court: 'ct',
  place: 'pl',
  terrace: 'ter',
  circle: 'cir',
  parkway: 'pkwy',
  highway: 'hwy',
  square: 'sq',
  trail: 'trl',
  north: 'n',
  south: 's',
  east: 'e',
  west: 'w',
};

/**
 * A trailing unit designator: "Unit 101", "Apt. 101", "#101", "No. 5", "Ste 200".
 * The unit number is captured either way — worded or bare-`#`.
 *
 * One pattern, two consumers with opposite needs: `slugify` canonicalizes the
 * match so every spelling of one condo produces one id, while `geocodeQuery`
 * strips it entirely (a geocoder resolves buildings, not apartments). Sharing
 * the constant is what keeps those two from drifting apart on which spellings
 * they recognize.
 */
export const UNIT_DESIGNATOR =
  /,?\s*(?:\b(?:unit|apt|apartment|ste|suite|no|rm|fl)\.?\s*#?\s*([\w-]+)|#\s*([\w-]+))\s*$/i;

/**
 * Collapse every spelling of a unit to one form, so "#101", "Apt 101", and
 * "Unit 101" are the same home. Without this, punctuation-stripping alone
 * yields a different id per spelling — and a re-scrape from another source
 * files a second, unannotated record instead of refreshing the first.
 */
function canonicalizeUnit(address: string): string {
  return address.replace(UNIT_DESIGNATOR, (_match, worded, hashed) => ` unit ${worded ?? hashed}`);
}

function normalizeWords(value: string): string {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, ' ')
    .split(' ')
    .filter(Boolean)
    .map((word) => SUFFIXES[word] ?? word)
    .join('-');
}

/**
 * The dedup key. Same house written any reasonable way → same slug.
 *
 * Keyed on zip, never city, because listing sites disagree about what "city"
 * means: Compass's detail page reports `addressLocality` as the *neighborhood*
 * ("Noe Valley") while its search page reports the city ("San Francisco"), so a
 * city key files one house twice depending on which page it came from.
 *
 * There is deliberately no city fallback — a key with two possible forms is the
 * same bug in a different costume, since the same house would land under a
 * different id depending on whether the scrape found a zip. `coerceScraped`
 * requires a zip instead, and fails loudly without one.
 */
export function slugify(parts: { address: string; state: string; zip: string }): string {
  return [canonicalizeUnit(parts.address), parts.zip, parts.state]
    .map(normalizeWords)
    .filter(Boolean)
    .join('-');
}

export function emptyStoreText(): string {
  return serializeStore([]);
}

export function serializeStore(rows: Property[]): string {
  return `${HEADER}\n${JSON.stringify(rows, null, 2)}\n`;
}

/**
 * Parse `data.js`. Throws on anything unexpected — this file is irreplaceable
 * user data, so "recovering" by returning an empty store would silently destroy
 * their history. A loud failure is always the better outcome here.
 */
export function parseStore(text: string): Property[] {
  if (text.trim() === '') {
    throw new Error('data.js is empty — refusing to treat that as an empty store');
  }
  const firstBreak = text.indexOf('\n');
  const firstLine = firstBreak === -1 ? text : text.slice(0, firstBreak);
  if (!firstLine.includes('window.PROPERTIES')) {
    throw new Error(
      `data.js is malformed: expected it to start with "${HEADER}", got ${JSON.stringify(firstLine.slice(0, 60))}`,
    );
  }
  let parsed: unknown;
  try {
    parsed = JSON.parse(text.slice(firstBreak + 1));
  } catch (err) {
    throw new Error(`data.js contains malformed JSON: ${(err as Error).message}`);
  }
  if (!Array.isArray(parsed)) {
    throw new Error(`data.js must contain a JSON array, got ${typeof parsed}`);
  }
  return parsed as Property[];
}

export function dataFile(dir: string): string {
  return path.join(dir, 'data.js');
}

/**
 * The one way to read the store, and the one place that says what to do when
 * there isn't one. Callers that need to fail before doing expensive work just
 * call this early — an existence-only preflight would let a *damaged* store
 * through and spend the browser run before failing anyway.
 */
export function readStore(dir: string): Property[] {
  const file = dataFile(dir);
  if (!fs.existsSync(file)) {
    // Deliberately not a command: the caller's cwd is unknown, and a
    // cwd-relative "node properties.ts init" fails with MODULE_NOT_FOUND from
    // anywhere but scripts/. SKILL.md carries the absolute invocation.
    throw new Error(`no store at ${dir} — run the "First, always" init command in SKILL.md first`);
  }
  return parseStore(fs.readFileSync(file, 'utf8'));
}

/**
 * Rename is atomic, so a reader never sees a half-written store — which matters
 * because the map may have the file open. This is not a concurrency lock: two
 * simultaneous writers would still lose one update. Nothing here writes
 * concurrently (one agent, one command at a time), so a lock would be cost
 * without benefit.
 */
export function writeStore(dir: string, rows: Property[]): void {
  const tmp = path.join(dir, `.data.js.tmp-${process.pid}`);
  fs.writeFileSync(tmp, serializeStore(rows));
  fs.renameSync(tmp, dataFile(dir));
}

/** Create or refresh. Replaces `scraped` wholesale; preserves `mine` exactly. */
export function upsertScraped(
  rows: Property[],
  scraped: Scraped,
  now: string = new Date().toISOString(),
): Property[] {
  const id = slugify(scraped);
  const index = rows.findIndex((row) => row.id === id);
  if (index === -1) {
    return [...rows, { id, scraped, mine: { rating: null, status: 'new', notes: '', added_at: now } }];
  }
  const next = rows.slice();
  next[index] = { id, scraped, mine: rows[index].mine };
  return next;
}

/**
 * Write one user-owned field. Scraped fields are deliberately unreachable here:
 * they may only come from a scrape, so `last_scraped_at` never lies about where
 * a value came from.
 */
export function setMine(rows: Property[], id: string, field: string, value: string): Property[] {
  if (!(MINE_FIELDS as readonly string[]).includes(field)) {
    throw new Error(
      `cannot set ${JSON.stringify(field)} — settable fields are ${MINE_FIELDS.join(', ')} ` +
        '(everything else comes from a scrape)',
    );
  }
  const index = rows.findIndex((row) => row.id === id);
  if (index === -1) {
    throw new Error(`no property with id ${JSON.stringify(id)}`);
  }

  const mine: Mine = { ...rows[index].mine };
  if (field === 'rating') {
    const rating = Number(value);
    if (!/^\d+$/.test(value.trim()) || !Number.isInteger(rating) || rating < 1 || rating > 5) {
      throw new Error(`rating must be a whole number from 1 to 5, got ${JSON.stringify(value)}`);
    }
    mine.rating = rating;
  } else if (field === 'status') {
    mine.status = value;
  } else if (field === 'notes') {
    mine.notes = value;
  } else {
    // Reachable only if MINE_FIELDS gains an entry without a branch here.
    // Failing beats silently writing the new field's value into notes.
    throw new Error(`${field} is listed as settable but has no write path`);
  }

  const next = rows.slice();
  next[index] = { ...rows[index], mine };
  return next;
}

/**
 * Validate and normalize agent-supplied JSON into a Scraped record. The agent
 * writes this by hand, so every field is checked here rather than trusted —
 * a bad address would silently create a duplicate house under a wrong slug.
 */
export function coerceScraped(input: unknown): Scraped {
  if (typeof input !== 'object' || input === null || Array.isArray(input)) {
    throw new Error('scraped payload must be a JSON object');
  }
  const raw = input as Record<string, unknown>;

  for (const key of ['address', 'state', 'zip'] as const) {
    if (typeof raw[key] !== 'string' || (raw[key] as string).trim() === '') {
      throw new Error(`scraped.${key} is required and must be a non-empty string — it forms the dedup key`);
    }
  }
  if (typeof raw.city !== 'string' || raw.city.trim() === '') {
    throw new Error('scraped.city is required and must be a non-empty string');
  }
  // Punctuation-only text passes the non-empty check but normalizes away,
  // which would silently merge unrelated houses under a truncated key.
  if (normalizeWords(raw.address as string) === '') {
    throw new Error(`scraped.address has no usable characters: ${JSON.stringify(raw.address)}`);
  }
  if (typeof raw.listing_url !== 'string' || !/^https?:\/\//i.test(raw.listing_url)) {
    throw new Error('scraped.listing_url is required and must be an http(s) URL');
  }
  const listingUrl = raw.listing_url;

  const asNumber = (key: string): number | null => {
    const value = raw[key];
    if (value === undefined || value === null || value === '') return null;
    const parsed = Number(value);
    if (!Number.isFinite(parsed)) {
      throw new Error(`scraped.${key} must be a number or null, got ${JSON.stringify(value)}`);
    }
    return parsed;
  };
  const asText = (key: string): string | null => {
    const value = raw[key];
    if (value === undefined || value === null || value === '') return null;
    return String(value);
  };

  // `rm` deletes this path relative to the properties folder, and the agent
  // that writes it also reads untrusted listing pages — so it must not be able
  // to name a file outside photos/.
  const photo = asText('photo');
  if (photo !== null && !/^photos\/[A-Za-z0-9._-]+$/.test(photo)) {
    throw new Error(`scraped.photo must be a plain filename under photos/, got ${JSON.stringify(photo)}`);
  }

  return {
    address: (raw.address as string).trim(),
    city: (raw.city as string).trim(),
    state: (raw.state as string).trim(),
    zip: (raw.zip as string).trim(),
    lat: asNumber('lat'),
    lng: asNumber('lng'),
    price: asNumber('price'),
    beds: asNumber('beds'),
    baths: asNumber('baths'),
    sqft: asNumber('sqft'),
    property_type: asText('property_type'),
    listing_status: asText('listing_status'),
    listing_url: listingUrl,
    // Any host is supported; the source label just falls out of the URL.
    listing_source: asText('listing_source') ?? new URL(listingUrl).hostname.replace(/^www\./, ''),
    photo,
    last_scraped_at: asText('last_scraped_at') ?? new Date().toISOString(),
  };
}

export function removeProperty(rows: Property[], id: string): Property[] {
  if (!rows.some((row) => row.id === id)) {
    throw new Error(`no property with id ${JSON.stringify(id)}`);
  }
  return rows.filter((row) => row.id !== id);
}
