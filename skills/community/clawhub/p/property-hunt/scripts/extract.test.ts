import { test } from 'node:test';
import assert from 'node:assert/strict';
import * as fs from 'node:fs';
import { fileURLToPath } from 'node:url';

import {
  extractScraped,
  flattenJsonLd,
  parseAddressLine,
  parseDescription,
  geocodeQuery,
  toNumber,
} from './extract.ts';
import type { PageSurfaces } from './extract.ts';
import { coerceScraped, slugify } from './store.ts';

// Captured from a live Compass detail page on 2026-08-14, trimmed to the
// surfaces the parser actually reads.
const COMPASS: PageSurfaces = JSON.parse(
  fs.readFileSync(fileURLToPath(new URL('./fixtures/compass-detail.json', import.meta.url)), 'utf8'),
);

test('a real Compass listing parses into the record the map needs', () => {
  const { scraped, photoUrl } = extractScraped(COMPASS, '2026-08-14T19:00:00.000Z');

  assert.equal(scraped.address, '424 28th St');
  assert.equal(scraped.city, 'San Francisco', 'the city, not the "Noe Valley" neighborhood JSON-LD reports');
  assert.equal(scraped.state, 'CA');
  assert.equal(scraped.zip, '94131');
  assert.equal(scraped.price, 3250000);
  assert.equal(scraped.beds, 3);
  assert.equal(scraped.baths, 3);
  assert.equal(scraped.sqft, 2315, 'floorSize arrives as the string "2,315 "');
  assert.equal(scraped.property_type, 'SingleFamilyResidence');
  assert.equal(scraped.listing_status, 'active', 'schema.org InStock is not a phrase to show a user');
  assert.equal(scraped.listing_source, 'compass.com');
  assert.match(scraped.listing_url, /424-28th-St-San-Francisco-CA-94131/);
  assert.ok(photoUrl && photoUrl.startsWith('https://'), 'a hero image is needed for the pin');
  assert.equal(scraped.lat, null, 'coordinates are not on this page — scrape.ts geocodes them');
  assert.equal(scraped.last_scraped_at, '2026-08-14T19:00:00.000Z');
});

test('the parsed record produces the id the store expects', () => {
  const { scraped } = extractScraped(COMPASS);
  assert.equal(slugify(scraped), '424-28th-st-94131-ca');
});

test('a listing with no usable address fails loudly instead of saving a blank house', () => {
  assert.throws(
    () => extractScraped({ url: 'https://example.com/x', jsonld: [], og: {} }),
    /could not find an address/,
  );
});

test('a listing that cannot be keyed is rejected by the same rules that save it', () => {
  // extract is lenient — it reports what the page had. scrape.ts runs the
  // result through coerceScraped before geocoding or downloading anything, so
  // an unsaveable listing fails immediately instead of after the expensive
  // work, leaving an orphaned photo behind.
  const { scraped } = extractScraped({
    url: 'https://example.com/y',
    jsonld: [
      {
        '@type': 'SingleFamilyResidence',
        url: 'https://example.com/y',
        // Everything present EXCEPT postalCode, so this pins the zip rule
        // specifically — with addressRegion missing too, the check would trip
        // on `state` first and stay green even if the zip rule were deleted.
        address: {
          '@type': 'PostalAddress',
          streetAddress: '12 Elm St',
          addressLocality: 'Springfield',
          addressRegion: 'IL',
        },
      },
    ],
    og: { 'og:title': '12 Elm St — For Sale' },
  });
  assert.equal(scraped.zip, '', 'the page genuinely had no zip');
  assert.equal(scraped.state, 'IL', 'everything else the key needs is present');
  assert.throws(() => coerceScraped(scraped), /scraped\.zip is required/);
});

// --- The pieces, so a failure points at which surface changed ---------------

test('json-ld arrives in three shapes and all of them flatten', () => {
  const node = { '@type': 'SingleFamilyResidence', name: 'x' };
  assert.equal(flattenJsonLd([node]).length, 1, 'bare object');
  assert.equal(flattenJsonLd([[node, node]]).length, 2, 'array');
  assert.equal(flattenJsonLd([{ '@context': 'x', '@graph': [node, node] }]).length, 2, '@graph wrapper');
});

test('numbers survive the formats listing sites actually emit', () => {
  assert.equal(toNumber('2,315 '), 2315);
  assert.equal(toNumber('$3,250,000'), 3250000);
  assert.equal(toNumber(3250000), 3250000);
  assert.equal(toNumber('3'), 3);
  assert.equal(toNumber(''), null);
  assert.equal(toNumber(null), null);
  assert.equal(toNumber('n/a'), null);
});

test('the canonical address line parses, with or without a trailing MLS number', () => {
  assert.deepEqual(parseAddressLine('424 28th St, San Francisco, CA 94131 | MLS #426153785'), {
    address: '424 28th St',
    city: 'San Francisco',
    state: 'CA',
    zip: '94131',
  });
  assert.deepEqual(parseAddressLine('1501 Greenwich St Unit 101, San Francisco, CA 94123'), {
    address: '1501 Greenwich St Unit 101',
    city: 'San Francisco',
    state: 'CA',
    zip: '94123',
  });
  assert.equal(parseAddressLine('Homes for Sale in San Francisco'), null);
});

test('the generated blurb yields the facts even when json-ld is thin', () => {
  assert.deepEqual(
    parseDescription(
      '424 28th St, San Francisco, CA 94131 is a single family home that will be listed for sale ' +
        'at $3,250,000. This is a 3-bed, 3-bath, 2,315 sqft property.',
    ),
    { price: 3250000, beds: 3, baths: 3, sqft: 2315 },
  );
});

test('a condo geocodes by its building, keeping the unit in the address', () => {
  // Observed live: Nominatim returns nothing for "1501 Greenwich St, Unit 101"
  // but resolves the building fine, which is the right pin either way.
  const sf = { city: 'San Francisco', state: 'CA', zip: '94123' };
  const expected = '1501 Greenwich St, San Francisco, CA, 94123';
  for (const address of [
    '1501 Greenwich St, Unit 101',
    '1501 Greenwich St Unit 101',
    '1501 Greenwich St #101',
    '1501 Greenwich St, Apt 101',
    '1501 Greenwich St, Apt. 101',
    '1501 Greenwich St, Ste 101',
    '1501 Greenwich St, Ste. 101',
    '1501 Greenwich St Unit#101',
    '1501 Greenwich St, No. 101',
  ]) {
    assert.equal(geocodeQuery({ ...sf, address }), expected, `${address} should geocode by building`);
  }
});

test('a plain street address is passed to the geocoder untouched', () => {
  assert.equal(
    geocodeQuery({ address: '424 28th St', city: 'San Francisco', state: 'CA', zip: '94131' }),
    '424 28th St, San Francisco, CA, 94131',
  );
});

test('a non-Compass listing parses from open-graph alone', () => {
  // listing_url accepts any host, so the parser must not depend on Compass's
  // JSON-LD shape being present at all.
  const { scraped } = extractScraped({
    url: 'https://www.zillow.com/homedetails/99-Oak-St-Oakland-CA-94609/12345_zpid/',
    jsonld: [],
    og: {
      'og:title': '99 Oak St, Oakland, CA 94609',
      'og:description': '99 Oak St, Oakland, CA 94609 is a home listed for sale at $985,000. This is a 2-bed, 1-bath, 1,100 sqft property.',
      'og:image': 'https://photos.zillowstatic.com/x.jpg',
    },
  });
  assert.equal(scraped.city, 'Oakland');
  assert.equal(scraped.price, 985000);
  assert.equal(scraped.beds, 2);
  assert.equal(scraped.sqft, 1100);
  assert.equal(scraped.listing_source, 'zillow.com');
});
