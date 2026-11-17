// Uber Eats (ubereats.com, Germany) provider.
//
// Uber Eats' consumer web app serves read-only discovery through open JSON
// endpoints (verified live, July 2026). They are POST-shaped queries but carry
// no auth, no session, and no identity:
//
//   feed   POST https://www.ubereats.com/api/getFeedV1?localeCode=de
//   store  POST https://www.ubereats.com/api/getStoreV1?localeCode=de
//   item   POST https://www.ubereats.com/api/getMenuItemV1?localeCode=de
//
// The delivery location travels in the `uev2.loc` cookie, a plain preference
// value the web app builds from user input (lat/lng only here, no identity).
// The `x-csrf-token: x` literal is the API's documented anonymous formality.
//
// READ-ONLY: no code path authenticates, creates a basket, orders, or pays.
// All Uber Eats prices are already integer cents.

import { CliError, CODES } from '../errors.js';
import { geocodeAddress } from '../geocode.js';

const BASE = process.env.UBEREATS_API_BASE || 'https://www.ubereats.com/api';

// ---- helpers ----------------------------------------------------------------

function locationHeaders(loc) {
  if (loc?.lat == null || loc?.lng == null) return {};
  const cookie = encodeURIComponent(JSON.stringify({ latitude: loc.lat, longitude: loc.lng }));
  return { cookie: `uev2.loc=${cookie}` };
}

function baseHeaders(loc) {
  return { 'x-csrf-token': 'x', ...locationHeaders(loc) };
}

/** "2,00 € Liefergebühr" -> 200; returns null when unparseable. */
function parseEuroTextToCents(text) {
  const m = /(\d+)[,.](\d{2})\s*€/.exec(text ?? '');
  if (!m) return null;
  return Number(m[1]) * 100 + Number(m[2]);
}

/** "30 Min." / "25–35 Min." -> {min, max}; nulls when unparseable. */
function parseEtaText(text) {
  const nums = (text ?? '').match(/\d+/g)?.map(Number) ?? [];
  if (nums.length === 0) return { min: null, max: null };
  return { min: nums[0], max: nums[nums.length - 1] ?? nums[0] };
}

function slugFromActionUrl(actionUrl) {
  const m = /\/store\/([^/]+)\//.exec(actionUrl ?? '');
  return m ? m[1] : null;
}

function normalizeFeedStore(store) {
  const meta = Array.isArray(store?.meta) ? store.meta : [];
  const fare = meta.find((b) => b?.badgeType === 'FARE');
  const etd = meta.find((b) => b?.badgeType === 'ETD');
  const eta = parseEtaText(etd?.text);
  return {
    id: store?.storeUuid ?? null,
    slug: slugFromActionUrl(store?.actionUrl),
    name: store?.title?.text ?? null,
    cuisines: [],
    rating: {
      score: store?.rating?.text != null ? Number(store.rating.text) : null,
      votes: null,
    },
    open: {
      // The feed only lists currently orderable stores; a closed state is not
      // exposed per store here.
      delivery: true,
      pickup: null,
    },
    delivery: {
      fee_cents: parseEuroTextToCents(fare?.badgeData?.fare?.deliveryFee ?? fare?.text),
      min_order_cents: null,
      eta_min: eta.min,
      eta_max: eta.max,
    },
    distance_m: null,
    address: { city: null, street: null, postcode: null },
    deals: [],
  };
}

function normalizeCatalogItem(item) {
  return {
    id: item?.uuid ?? null,
    name: item?.title ?? null,
    description: item?.itemDescription || null,
    sold_out: item?.isSoldOut ?? null,
    has_options: item?.hasCustomizations ?? null,
    variants: [
      {
        id: item?.uuid ?? null,
        name: item?.title ?? null,
        price_cents: Number.isFinite(item?.price) ? item.price : null,
        option_group_ids: [],
      },
    ],
  };
}

function normalizeCustomization(c) {
  return {
    id: c?.uuid ?? null,
    name: c?.title ?? null,
    min_choices: c?.minPermitted ?? null,
    max_choices: c?.maxPermitted ?? null,
    options: (c?.options ?? []).map((o) => ({
      id: o?.uuid ?? null,
      name: o?.title ?? null,
      price_cents: Number.isFinite(o?.price) ? o.price : 0,
      min_amount: o?.minPermitted ?? null,
      max_amount: o?.maxPermitted ?? null,
    })),
  };
}

function catalogSections(storeData) {
  // catalogSectionsMap can hold several entries (e.g. one per dining mode) in
  // varying order, some empty; use the richest one.
  const map = storeData?.catalogSectionsMap ?? {};
  let best = [];
  for (const v of Object.values(map)) {
    if (Array.isArray(v) && v.length > best.length) best = v;
  }
  return best;
}

// ---- provider ---------------------------------------------------------------

/**
 * @param {{http: {getJson: Function, postJson: Function}}} deps
 */
export function createUberEatsProvider({ http }) {
  const name = 'ubereats';

  async function ensureLatLng(loc) {
    if (loc?.lat != null && loc?.lng != null) return loc;
    if (!loc?.postcode) {
      throw new CliError(CODES.INVALID_ARGUMENT, 'Uber Eats discovery needs --address or --postcode.', {
        provider: name,
        exitCode: 2,
      });
    }
    const g = await geocodeAddress(`${loc.postcode}, Deutschland`, { http });
    return { ...loc, lat: g.lat, lng: g.lng };
  }

  async function fetchFeed(loc) {
    const doc = await http.postJson(`${BASE}/getFeedV1?localeCode=de`, {
      headers: baseHeaders(loc),
      body: { pageInfo: { offset: 0, pageSize: 80 } },
    });
    const items = doc?.data?.feedItems ?? [];
    const seen = new Set();
    const stores = [];
    for (const item of items) {
      if (item?.type !== 'REGULAR_STORE' || !item?.store?.storeUuid) continue;
      if (seen.has(item.store.storeUuid)) continue;
      seen.add(item.store.storeUuid);
      stores.push(normalizeFeedStore(item.store));
    }
    return stores;
  }

  async function fetchStore(storeUuid, loc = null) {
    if (!storeUuid) {
      throw new CliError(CODES.INVALID_ARGUMENT, 'A store id (UUID from search output) is required.', {
        provider: name,
        exitCode: 2,
      });
    }
    const doc = await http.postJson(`${BASE}/getStoreV1?localeCode=de`, {
      headers: baseHeaders(loc),
      body: { storeUuid, diningMode: 'DELIVERY' },
    });
    const data = doc?.data;
    if (doc?.status === 'failure' || !data?.title) {
      // Uber Eats reports API-level failures inside an HTTP 200. A "404" here
      // can also be transient soft throttling, hence retryable.
      throw new CliError(
        CODES.NOT_FOUND,
        `Store ${storeUuid} was not returned. Check the id from search output; this can also be transient throttling, retry once after a pause.`,
        { provider: name, retryable: true }
      );
    }
    return data;
  }

  return {
    name,

    async searchRestaurants(loc, { query = null, limit = 25, openNow = false } = {}) {
      const resolved = await ensureLatLng(loc);
      let list = await fetchFeed(resolved);
      // The feed already excludes closed stores, so openNow is a no-op here.
      void openNow;
      if (query) {
        const q = query.toLowerCase();
        list = list.filter((r) => (r.name ?? '').toLowerCase().includes(q) || (r.slug ?? '').includes(q));
      }
      const total = list.length;
      if (limit > 0) list = list.slice(0, limit);
      return {
        location: { postcode: loc.postcode ?? null },
        total_matches: total,
        returned: list.length,
        restaurants: list,
      };
    },

    async getRestaurant(idOrSlug, loc = null) {
      const resolved = loc ? await ensureLatLng(loc) : null;
      const data = await fetchStore(idOrSlug, resolved);
      const eta = parseEtaText(data?.etaRange?.text);
      return {
        id: idOrSlug,
        slug: data?.slug ?? null,
        name: data?.title ?? null,
        rating: {
          score: data?.rating?.ratingValue ?? null,
          votes: data?.rating?.reviewCount ?? null,
        },
        open: {
          // Without a delivery location the API reports a closed-style message
          // for any store, so only trust it when a location was provided.
          delivery: data?.closedMessage ? (resolved ? false : null) : true,
          pickup: null,
        },
        delivery: {
          fee_cents: null,
          min_order_cents: null,
          eta_min: eta.min,
          eta_max: eta.max,
          service_fee_cents: data?.fareInfo?.serviceFeeCents ?? null,
        },
        address: {
          city: data?.location?.city ?? null,
          street: data?.location?.streetAddress ?? null,
          postcode: data?.location?.postalCode ?? null,
        },
        currency: data?.currencyCode ?? 'EUR',
        cuisines: data?.cuisineList ?? [],
      };
    },

    async getMenu(idOrSlug, { category = null, includeOptions = false } = {}) {
      if (includeOptions) {
        throw new CliError(
          CODES.INVALID_ARGUMENT,
          'Uber Eats resolves option groups per item; use the item command instead of --include-options.',
          { provider: name, exitCode: 2 }
        );
      }
      const data = await fetchStore(idOrSlug);
      let categories = catalogSections(data)
        .map((s) => {
          const payload = s?.payload?.standardItemsPayload ?? {};
          return {
            id: s?.catalogSectionUUID ?? null,
            name: payload?.title?.text ?? null,
            items: (payload?.catalogItems ?? []).map(normalizeCatalogItem),
          };
        })
        .filter((c) => c.items.length > 0);
      if (category) {
        const q = String(category).toLowerCase();
        categories = categories.filter((c) => String(c.id).toLowerCase() === q || (c.name ?? '').toLowerCase().includes(q));
        if (categories.length === 0) {
          throw new CliError(CODES.NOT_FOUND, `No menu category matches "${category}".`, { provider: name });
        }
      }
      return {
        restaurant_slug: idOrSlug,
        restaurant_name: data?.title ?? null,
        currency: data?.currencyCode ?? 'EUR',
        category_count: categories.length,
        item_count: categories.reduce((n, c) => n + c.items.length, 0),
        categories,
        note: 'Item ids repeat across sections when a dish appears in multiple carousels.',
      };
    },

    async getItem(idOrSlug, itemId) {
      if (!itemId) {
        throw new CliError(CODES.INVALID_ARGUMENT, 'An item id is required.', { provider: name, exitCode: 2 });
      }
      const data = await fetchStore(idOrSlug);
      let found = null;
      for (const s of catalogSections(data)) {
        const payload = s?.payload?.standardItemsPayload ?? {};
        for (const item of payload?.catalogItems ?? []) {
          if (String(item?.uuid) === String(itemId)) {
            found = { item, sectionUuid: item?.sectionUuid ?? s?.catalogSectionUUID ?? '', subsectionUuid: item?.subsectionUuid ?? '' };
            break;
          }
        }
        if (found) break;
      }
      if (!found) {
        // Promo carousels rotate between fetches and can carry their own item
        // uuids, so an id from an older menu snapshot may be gone. Never call
        // getMenuItemV1 without section context (the API rejects it).
        throw new CliError(
          CODES.NOT_FOUND,
          `Item ${itemId} is not in the current catalog of store ${idOrSlug}. Re-run the menu command and use a fresh item id (prefer canonical categories over promo carousels).`,
          { provider: name, retryable: true }
        );
      }
      // The web client always browses a store with a uev2.loc cookie set;
      // mirror that by using the store's own coordinates as location context.
      const storeLoc =
        data?.location?.latitude != null && data?.location?.longitude != null
          ? { lat: data.location.latitude, lng: data.location.longitude }
          : null;
      const detail = await http.postJson(`${BASE}/getMenuItemV1?localeCode=de`, {
        headers: baseHeaders(storeLoc),
        body: {
          storeUuid: idOrSlug,
          menuItemUuid: itemId,
          sectionUuid: found.sectionUuid,
          subsectionUuid: found.subsectionUuid,
        },
      });
      const d = detail?.data ?? {};
      const optionGroups = (d?.customizationsList ?? []).map(normalizeCustomization);
      return {
        restaurant_slug: idOrSlug,
        currency: data?.currencyCode ?? 'EUR',
        item: {
          id: itemId,
          name: d?.title ?? found.item?.title ?? null,
          description: d?.itemDescription || found.item?.itemDescription || null,
          variants: [
            {
              id: itemId,
              name: d?.title ?? found.item?.title ?? null,
              price_cents: Number.isFinite(d?.price) ? d.price : found.item?.price ?? null,
              option_group_ids: optionGroups.map((g) => g.id),
              option_groups: optionGroups,
            },
          ],
        },
      };
    },

    async availability(loc) {
      const resolved = await ensureLatLng(loc);
      const list = await fetchFeed(resolved);
      return {
        location: { postcode: loc.postcode ?? null },
        restaurant_count: list.length,
        open_for_delivery: list.length,
        open_for_pickup: null,
        closed: null,
        deliverable: list.length > 0,
        note: 'The Uber Eats feed only lists currently orderable stores; closed stores are not counted.',
      };
    },
  };
}
