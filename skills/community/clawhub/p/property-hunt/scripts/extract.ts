// Pure listing parser. No browser, no network — scrape.ts hands it the page's
// structured surfaces and it hands back a record. Kept separate precisely so it
// can be tested against fixtures.
//
// It reads only standards-based surfaces: schema.org JSON-LD and Open Graph
// meta. No DOM selectors anywhere, which is what keeps it working across a
// cosmetic redesign — and what lets it generalize past Compass, since
// listing_url accepts any host.
import { UNIT_DESIGNATOR } from './store.ts';
import type { Scraped } from './store.ts';

export type PageSurfaces = {
  url: string;
  jsonld: unknown[];
  og: Record<string, string>;
};

const RESIDENCE_TYPES = [
  'SingleFamilyResidence',
  'RealEstateListing',
  'Residence',
  'Apartment',
  'House',
  'Product',
];

/** JSON-LD arrives as arrays, single objects, or @graph wrappers. Flatten all three. */
export function flattenJsonLd(blocks: unknown[]): Record<string, unknown>[] {
  const out: Record<string, unknown>[] = [];
  const visit = (node: unknown): void => {
    if (Array.isArray(node)) {
      node.forEach(visit);
      return;
    }
    if (node === null || typeof node !== 'object') return;
    const obj = node as Record<string, unknown>;
    if (Array.isArray(obj['@graph'])) {
      (obj['@graph'] as unknown[]).forEach(visit);
      return;
    }
    if (obj['@type'] !== undefined) out.push(obj);
  };
  blocks.forEach(visit);
  return out;
}

function typesOf(node: Record<string, unknown>): string[] {
  const raw = node['@type'];
  return (Array.isArray(raw) ? raw : [raw]).filter((t): t is string => typeof t === 'string');
}

/** Numbers arrive as "2,315 ", "3", 3250000 — normalize all of them. */
export function toNumber(value: unknown): number | null {
  if (value === null || value === undefined) return null;
  if (typeof value === 'number') return Number.isFinite(value) ? value : null;
  const cleaned = String(value).replace(/[,\s$]/g, '');
  if (cleaned === '') return null;
  const parsed = Number(cleaned);
  return Number.isFinite(parsed) ? parsed : null;
}

function firstDeep(node: unknown, key: string): unknown {
  if (Array.isArray(node)) {
    for (const item of node) {
      const found = firstDeep(item, key);
      if (found !== undefined) return found;
    }
    return undefined;
  }
  if (node === null || typeof node !== 'object') return undefined;
  const obj = node as Record<string, unknown>;
  if (obj[key] !== undefined) return obj[key];
  for (const value of Object.values(obj)) {
    const found = firstDeep(value, key);
    if (found !== undefined) return found;
  }
  return undefined;
}

/**
 * Parse the canonical address line listing sites put in og:title / og:description:
 *   "424 28th St, San Francisco, CA 94131 | MLS #426153785"
 * Preferred over JSON-LD's PostalAddress because addressLocality is often the
 * neighborhood ("Noe Valley") rather than the city.
 */
export function parseAddressLine(line: string): {
  address: string;
  city: string;
  state: string;
  zip: string;
} | null {
  const head = line.split('|')[0].trim();
  const match = head.match(/^(.+?),\s*([^,]+?),\s*([A-Z]{2})\s+(\d{5})(?:-\d{4})?\s*$/);
  if (!match) return null;
  return { address: match[1].trim(), city: match[2].trim(), state: match[3], zip: match[4] };
}

/** "…3-bed, 3-bath, 2,315 sqft property." — the generated blurb every site writes. */
export function parseDescription(description: string): {
  price: number | null;
  beds: number | null;
  baths: number | null;
  sqft: number | null;
} {
  const grab = (re: RegExp): number | null => toNumber(description.match(re)?.[1] ?? null);
  return {
    price: grab(/\$\s*([\d,]+)/),
    beds: grab(/([\d.]+)[-\s]*bed/i),
    baths: grab(/([\d.]+)[-\s]*bath/i),
    sqft: grab(/([\d,]+)\s*sq\.?\s*ft/i),
  };
}

/**
 * The address as a geocoder wants it. Unit designators have to come off: a
 * geocoder resolves buildings, not apartments, and "1501 Greenwich St, Unit
 * 101" returns nothing while "1501 Greenwich St" resolves fine. The building's
 * coordinates are what a map pin wants anyway.
 *
 * The unit stays in `scraped.address` — it is part of the identity of the home
 * and part of the dedup key. Only the geocoder query drops it.
 */
export function geocodeQuery(parts: {
  address: string;
  city: string;
  state: string;
  zip: string;
}): string {
  const street = parts.address
    // Same designator pattern the store canonicalizes on — shared so the two
    // cannot disagree about what counts as a unit.
    .replace(UNIT_DESIGNATOR, '')
    .replace(/,\s*$/, '')
    .trim();
  return [street, parts.city, parts.state, parts.zip].filter(Boolean).join(', ');
}

function statusFrom(availability: unknown): string | null {
  if (typeof availability !== 'string') return null;
  const tail = availability.split('/').pop() ?? availability;
  const map: Record<string, string> = {
    InStock: 'active',
    LimitedAvailability: 'active',
    PreOrder: 'coming soon',
    SoldOut: 'sold',
    OutOfStock: 'off market',
    Discontinued: 'off market',
  };
  return map[tail] ?? tail;
}

/**
 * `scraped.photo` is a path *inside the properties folder*, so it can only be
 * filled after the image is downloaded. The remote URL comes back alongside it
 * rather than being crammed into the same field.
 */
export type Extracted = { scraped: Scraped; photoUrl: string | null };

/**
 * Build a record from a page's structured surfaces.
 *
 * `lat`/`lng` are left null here on purpose — coordinates are absent from every
 * structured surface on a Compass detail page (verified against a live page),
 * so scrape.ts resolves them by geocoding. Keeping the network out of here is
 * what keeps this function testable.
 */
export function extractScraped(page: PageSurfaces, now: string = new Date().toISOString()): Extracted {
  const nodes = flattenJsonLd(page.jsonld);
  const listing =
    nodes.find((node) => typesOf(node).some((t) => RESIDENCE_TYPES.includes(t) && t !== 'Product')) ??
    nodes.find((node) => typesOf(node).includes('Product'));

  const og = page.og;
  const blurb = og['og:description'] ?? og['twitter:description'] ?? '';
  const fromBlurb = parseDescription(blurb);

  const addressLine =
    parseAddressLine(og['og:title'] ?? '') ??
    parseAddressLine(og['twitter:title'] ?? '') ??
    parseAddressLine(blurb);

  const postal = listing ? (firstDeep(listing, 'address') as Record<string, unknown> | undefined) : undefined;
  const address =
    addressLine ??
    (postal
      ? {
          address: String(postal.streetAddress ?? '').trim(),
          city: String(postal.addressLocality ?? '').trim(),
          state: String(postal.addressRegion ?? '').trim(),
          zip: String(postal.postalCode ?? '').trim(),
        }
      : null);

  if (!address || address.address === '') {
    throw new Error(
      `could not find an address on ${page.url} — the page may not have finished rendering, ` +
        'or it is not a listing page',
    );
  }

  const offers = listing ? (firstDeep(listing, 'offers') as Record<string, unknown> | undefined) : undefined;
  const floorPlan = listing ? (firstDeep(listing, 'accommodationFloorPlan') as Record<string, unknown> | undefined) : undefined;
  const floorSize = listing ? firstDeep(listing, 'floorSize') : undefined;

  // og:url and JSON-LD url are sometimes site-relative; resolve against the page.
  const listingUrl = new URL(
    (typeof listing?.url === 'string' ? listing.url : undefined) ?? og['og:url'] ?? page.url,
    page.url,
  ).href;

  const image = listing ? firstDeep(listing, 'image') : undefined;
  const imageUrl =
    (typeof firstDeep(image, 'url') === 'string' ? (firstDeep(image, 'url') as string) : undefined) ??
    (typeof image === 'string' ? image : undefined) ??
    og['og:image'];

  const propertyType =
    listing ? typesOf(listing).find((t) => t !== 'Product' && t !== 'RealEstateListing') ?? null : null;

  return {
    scraped: {
      address: address.address,
      city: address.city,
      state: address.state,
      zip: address.zip,
      lat: null,
      lng: null,
      price: toNumber(offers?.price) ?? fromBlurb.price,
      beds: toNumber(floorPlan?.numberOfBedrooms) ?? fromBlurb.beds,
      baths: toNumber(floorPlan?.numberOfBathroomsTotal) ?? fromBlurb.baths,
      sqft: toNumber(firstDeep(floorSize, 'value')) ?? fromBlurb.sqft,
      property_type: propertyType,
      listing_status: statusFrom(offers?.availability),
      listing_url: listingUrl,
      listing_source: new URL(listingUrl).hostname.replace(/^www\./, ''),
      photo: null,
      last_scraped_at: now,
    },
    photoUrl: imageUrl ? new URL(imageUrl, page.url).href : null,
  };
}
