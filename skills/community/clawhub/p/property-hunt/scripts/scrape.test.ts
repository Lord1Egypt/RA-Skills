import { test } from 'node:test';
import assert from 'node:assert/strict';

import * as fs from 'node:fs';
import * as os from 'node:os';
import * as path from 'node:path';
import { execFileSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

import {
  isPrivateAddress,
  keepPreviousEnrichment,
  resolvePublicDestination,
  scrapeRendered,
} from './scrape.ts';
import type { Scraped } from './store.ts';

// A stand-in for the Camoufox proxy. Only `goto` and `eval` are used, and
// `eval` is dispatched on which surface the caller asked for — so a page can be
// made to render in stages, which is the whole point of the retry loop.
function fakeBrowser(states: Array<{ jsonld: unknown[]; og: Record<string, string> }>) {
  let poll = 0;
  return {
    polls: () => poll,
    async goto() {},
    async eval(expression: string) {
      // One harvest reads json-ld then og. Both must see the SAME state or the
      // fake invents a half-and-half page that never occurs in reality.
      const current = states[Math.min(poll, states.length - 1)];
      if (expression.includes('ld+json')) {
        return current.jsonld.map((block) => JSON.stringify(block));
      }
      poll += 1; // og is read second — advance only once the harvest is done
      return current.og;
    },
  };
}

// The give-up path waits out the full render budget, so tests pass a short one
// rather than sitting through the 45s production default.
const SHORT_TIMEOUT_MS = 2_000;

const URL_ = 'https://www.compass.com/homedetails/424-28th-St-San-Francisco-CA-94131/1QUY9H_pid/';

const RESIDENCE = {
  '@type': 'SingleFamilyResidence',
  url: URL_,
  address: {
    '@type': 'PostalAddress',
    streetAddress: '424 28th St',
    addressLocality: 'Noe Valley',
    addressRegion: 'CA',
    // no postalCode — the shape that made a half-rendered page fatal
  },
  offers: { '@type': 'Offer', price: 3250000, availability: 'https://schema.org/InStock' },
};

const FULL_OG = {
  'og:title': '424 28th St, San Francisco, CA 94131 | MLS #426153785',
  'og:description':
    '424 28th St, San Francisco, CA 94131 is a single family home that will be listed for sale ' +
    'at $3,250,000. This is a 3-bed, 3-bath, 2,315 sqft property.',
  'og:image': 'https://www.compass.com/m/abc/origin.jpg',
};

test('a page that renders in stages is retried, not abandoned', async () => {
  // Poll 1: JSON-LD has mounted (no postalCode) but og:title has not, so the
  // record is unkeyable. Poll 2: og:title arrives and it becomes saveable.
  // Before the retry landed inside the loop, poll 1 aborted the whole run.
  const browser = fakeBrowser([
    { jsonld: [RESIDENCE], og: {} },
    { jsonld: [RESIDENCE], og: FULL_OG },
  ]);

  const { scraped } = await scrapeRendered(browser, URL_);

  assert.equal(scraped.zip, '94131');
  assert.equal(scraped.city, 'San Francisco');
  assert.equal(scraped.price, 3250000);
  assert.ok(browser.polls() > 1, 'the first poll must not have been treated as final');
});

test('a page that never becomes saveable reports what was missing and where', async () => {
  const browser = fakeBrowser([{ jsonld: [RESIDENCE], og: {} }]);

  await assert.rejects(
    () => scrapeRendered(browser, URL_, SHORT_TIMEOUT_MS),
    (err: Error) => {
      assert.match(err.message, /could not read a saveable listing/);
      assert.match(err.message, /424-28th-St/, 'the URL is needed to act on this');
      assert.match(err.message, /zip is required/, 'and the actual blocker');
      assert.match(err.message, /another listing site/, 'a missing field is worth trying elsewhere');
      return true;
    },
  );
});

test('a browser failure is not reported as a missing field', async () => {
  // A bot wall or a browser that goes away mid-run lands in the same catch.
  // Telling the agent to "try another listing site" would send it after the
  // wrong problem entirely.
  const broken = {
    async goto() {},
    async eval() {
      throw Object.assign(new Error('connection refused'), { name: 'BrowserRpcError' });
    },
  };

  await assert.rejects(
    () => scrapeRendered(broken, URL_, SHORT_TIMEOUT_MS),
    (err: Error) => {
      assert.match(err.message, /connection refused/);
      assert.doesNotMatch(err.message, /another listing site/);
      return true;
    },
  );
});

test('scraping into an uninitialized folder costs nothing and says what to do', async () => {
  // The guard runs before connect(), so this needs no browser. Without it,
  // readStore raised a bare ENOENT *after* the browser run, the geocode, and a
  // photo download that had already created photos/ and an orphaned image.
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'property-hunt-uninit-'));
  const out = execFileSync(
    process.execPath,
    [fileURLToPath(new URL('./scrape.ts', import.meta.url)), 'https://example.com/listing/1'],
    { env: { ...process.env, PROPERTY_HUNT_DIR: dir }, encoding: 'utf8' },
  );

  const payload = JSON.parse(out.trim());
  assert.equal(payload.type, 'tool_error');
  assert.match(payload.error, /no store at/);
  assert.match(payload.error, /SKILL\.md/, 'points at the canonical init command rather than a cwd-relative one');
  assert.deepEqual(fs.readdirSync(dir), [], 'nothing may be written before the store is known to exist');
});

test('a refresh keeps only the enrichment this run failed to produce', () => {
  const build = (lat: number | null, lng: number | null, photo: string | null) =>
    ({ lat, lng, photo }) as Scraped;
  // Photo carry-forward is filesystem-backed and has its own test below; this
  // matrix covers the coordinate contract, so an empty dir is the right input.
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'property-hunt-coords-'));

  for (const { name, fresh, previous, kept, expected } of [
    {
      name: 'a transient geocoder failure keeps the last known coordinates',
      fresh: build(null, null, null),
      previous: build(37.745, -122.432, 'photos/x.jpg'),
      // Photo is absent from this dir, so it is correctly not carried — the
      // filesystem-backed case has its own test.
      kept: ['coordinates'],
      expected: [37.745, -122.432, null],
    },
    {
      name: 'a successful refresh still overwrites',
      fresh: build(9, 8, 'photos/new.jpg'),
      previous: build(1, 2, 'photos/old.jpg'),
      kept: [],
      expected: [9, 8, 'photos/new.jpg'],
    },
    {
      name: 'a new property has nothing to carry forward',
      fresh: build(null, null, null),
      previous: undefined,
      kept: [],
      expected: [null, null, null],
    },
  ]) {
    assert.deepEqual(keepPreviousEnrichment(fresh, previous, dir), kept, name);
    assert.deepEqual([fresh.lat, fresh.lng, fresh.photo], expected, name);
  }
});

// --- The image URL comes from the listing page, so it is attacker input ------

test('photo addresses are classified by routability, not by spelling', () => {
  for (const { expected, addresses } of [
    {
      expected: true,
      addresses: [
        '127.0.0.1', '127.1.2.3', '0.0.0.0', '10.0.0.5', '172.16.9.9', '172.31.255.1',
        '192.168.1.1', '169.254.169.254', '100.64.0.1', '224.0.0.1',
        '::1', '::', 'fc00::1', 'fd12::3', 'fe80::1', '[::1]',
        // Spellings the first version of this guard let through — one address
        // has many texts, so these are judged by value.
        '::ffff:127.0.0.1', '::ffff:7f00:1', '::ffff:0:7f00:1', '64:ff9b::7f00:1',
        '::ffff:a00:1', 'fe90::1', 'feb0::1',
      ],
    },
    {
      expected: false,
      addresses: [
        '93.184.216.34', '8.8.8.8', '172.32.0.1', '169.253.0.1',
        '2606:2800:220:1::1', '2001:4860:4860::8888', '::ffff:8.8.8.8', '::ffff:808:808',
      ],
    },
  ]) {
    for (const address of addresses) {
      assert.equal(isPrivateAddress(address), expected, `${address} should be ${expected ? 'refused' : 'allowed'}`);
    }
  }
});

test('a hostname that resolves inward is refused, not just a literal IP', async () => {
  // The realistic payload is a *name* — "localhost", or an attacker domain
  // whose A record points at 127.0.0.1 — so the guard resolves rather than
  // pattern-matching the URL text.
  await assert.rejects(() => resolvePublicDestination('http://localhost/x.jpg'), /non-public address/);
  await assert.rejects(() => resolvePublicDestination('http://127.0.0.1:9222/x.jpg'), /non-public address/);
  await assert.rejects(() => resolvePublicDestination('file:///etc/passwd'), /refusing a file: image URL/);
});

test('a redirect target is vetted against the same rule as the first hop', async () => {
  await assert.rejects(
    () => resolvePublicDestination('/internal', new URL('http://localhost/start')),
    /non-public address/,
  );
});

test('the vetted address is returned so the caller can pin to it', async () => {
  // Returning the address is what closes the rebinding window: validating a
  // name and letting the client resolve it again is two lookups, and the
  // attacker controls what the second one answers.
  const resolved = await resolvePublicDestination('http://93.184.216.34/x.jpg');
  assert.equal(resolved.address, '93.184.216.34');
  assert.equal(resolved.family, 4);
  assert.equal(resolved.url.hostname, '93.184.216.34');
});

test('a carried-forward photo must still exist on disk', () => {
  // Caught live: the download broke, the carry-forward kept the old path, and
  // the record pointed at a file that was gone — the map renders that as a
  // broken image, which is worse than the honest plain marker.
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'property-hunt-photo-'));
  fs.mkdirSync(path.join(dir, 'photos'));
  const fresh = { lat: 1, lng: 2, photo: null } as unknown as Scraped;
  const previous = { lat: 1, lng: 2, photo: 'photos/gone.jpg' } as Scraped;

  assert.deepEqual(keepPreviousEnrichment(fresh, previous, dir), [], 'nothing to carry when the file is gone');
  assert.equal(fresh.photo, null, 'better a plain marker than a broken image');

  fs.writeFileSync(path.join(dir, 'photos', 'gone.jpg'), 'bytes');
  const second = { lat: 1, lng: 2, photo: null } as unknown as Scraped;
  assert.deepEqual(keepPreviousEnrichment(second, previous, dir), ['photo']);
  assert.equal(second.photo, 'photos/gone.jpg');
});
