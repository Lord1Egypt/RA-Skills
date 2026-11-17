// Lieferando (lieferando.de, Just Eat Takeaway Germany) provider.
//
// Since the 2025/26 migration to the Just Eat platform, lieferando.de is served
// by two unauthenticated public JSON sources (verified live):
//
//   discovery  GET https://i18n.api.just-eat.io/discovery/de/restaurants/enriched/bypostcode/{postcode}
//   menu CDN   GET https://globalmenucdn.eu-central-1.production.jet-external.com/{uniqueName}_de_manifest.json
//              GET {cdn}/{ItemsUrl}          (items + variations, from manifest)
//              GET {cdn}/{ItemDetailsUrl}    (modifier groups/sets, from manifest)
//
// READ-ONLY: only these discovery/menu endpoints are implemented. There is
// deliberately no code path that authenticates, creates a platform basket,
// orders, or pays.
//
// Units: discovery `deliveryCost`/`minimumDeliveryValue` and all menu CDN
// prices (BasePrice, AdditionPrice) are float euros -> converted to integer
// cents here. `deliveryFees.restaurants[].bands` are already integer cents.

import { CliError, CODES } from '../errors.js';

const DISCOVERY_BASE = process.env.LIEFERANDO_DISCOVERY_BASE || 'https://i18n.api.just-eat.io';
const MENU_CDN_BASE = process.env.LIEFERANDO_MENUCDN_BASE || 'https://globalmenucdn.eu-central-1.production.jet-external.com';
const TENANT = 'de';

// ---- helpers ----------------------------------------------------------------

function eurosToCents(v) {
  if (v == null || !Number.isFinite(Number(v))) return null;
  return Math.round(Number(v) * 100);
}

function normalizeRestaurant(r, feeBands) {
  const bands = feeBands?.bands ?? null;
  return {
    id: r?.id ?? null,
    slug: r?.uniqueName ?? null,
    name: r?.name ?? null,
    cuisines: (r?.cuisines ?? []).map((c) => c?.uniqueName ?? c?.name).filter(Boolean),
    rating: {
      score: r?.rating?.starRating ?? null,
      votes: r?.rating?.count ?? null,
    },
    open: {
      delivery: r?.isOpenNowForDelivery ?? null,
      pickup: r?.isOpenNowForCollection ?? null,
      preorder: r?.isOpenNowForPreorder ?? null,
      temporarily_offline: r?.isTemporarilyOffline ?? null,
    },
    delivery: {
      fee_cents: eurosToCents(r?.deliveryCost),
      min_order_cents: eurosToCents(r?.minimumDeliveryValue),
      eta_min: r?.deliveryEtaMinutes?.rangeLower ?? null,
      eta_max: r?.deliveryEtaMinutes?.rangeUpper ?? null,
      fee_bands: bands, // integer cents: [{minimumAmount, fee}]
    },
    distance_m: r?.driveDistanceMeters ?? null,
    address: {
      city: r?.address?.city ?? null,
      street: r?.address?.firstLine ?? null,
      postcode: r?.address?.postalCode ?? null,
    },
    deals: (r?.deals ?? []).map((d) => d?.description).filter(Boolean),
  };
}

function normalizeModifierGroup(gid, groupsById, setsById) {
  const g = groupsById.get(String(gid));
  if (!g) return { id: gid, name: null, options: [] };
  return {
    id: g.Id,
    name: g.Name ?? null,
    min_choices: g.MinChoices ?? null,
    max_choices: g.MaxChoices ?? null,
    options: (g.Modifiers ?? [])
      .map((sid) => setsById.get(String(sid))?.Modifier)
      .filter(Boolean)
      .map((m) => ({
        id: m.Id ?? null,
        name: m.Name ?? null,
        price_cents: eurosToCents(m.AdditionPrice),
        min_amount: m.MinChoices ?? null,
        max_amount: m.MaxChoices ?? null,
      })),
  };
}

function normalizeItem(item, { details = null } = {}) {
  const groupsById = new Map((details?.ModifierGroups ?? []).map((g) => [String(g.Id), g]));
  const setsById = new Map((details?.ModifierSets ?? []).map((s) => [String(s.Id), s]));
  return {
    id: item?.Id ?? null,
    name: item?.Name ?? null,
    description: item?.Description || null,
    variants: (item?.Variations ?? []).map((v) => ({
      id: v?.Id ?? null,
      name: v?.Name ?? null,
      type: v?.Type ?? null,
      price_cents: eurosToCents(v?.BasePrice),
      deal_only: v?.DealOnly ?? false,
      option_group_ids: v?.ModifierGroupsIds ?? [],
      ...(details
        ? { option_groups: (v?.ModifierGroupsIds ?? []).map((gid) => normalizeModifierGroup(gid, groupsById, setsById)) }
        : {}),
    })),
  };
}

// ---- provider ---------------------------------------------------------------

/**
 * @param {{http: {getJson: Function}}} deps
 */
export function createLieferandoProvider({ http }) {
  const name = 'lieferando';

  async function fetchDiscovery(loc) {
    if (!loc?.postcode) {
      throw new CliError(CODES.INVALID_ARGUMENT, 'Lieferando discovery needs a German postcode.', {
        provider: name,
        exitCode: 2,
      });
    }
    const doc = await http.getJson(`${DISCOVERY_BASE}/discovery/${TENANT}/restaurants/enriched/bypostcode/${loc.postcode}`);
    const feeById = doc?.deliveryFees?.restaurants ?? {};
    const restaurants = (doc?.restaurants ?? [])
      .filter((r) => r?.isTestRestaurant !== true)
      .map((r) => normalizeRestaurant(r, feeById[r?.id]));
    return { restaurants, meta: doc?.metaData ?? {} };
  }

  async function fetchManifest(slug) {
    if (!slug) {
      throw new CliError(CODES.INVALID_ARGUMENT, 'A restaurant slug is required.', { provider: name, exitCode: 2 });
    }
    try {
      return await http.getJson(`${MENU_CDN_BASE}/${encodeURIComponent(slug)}_${TENANT}_manifest.json`);
    } catch (err) {
      if (err instanceof CliError && err.code === CODES.NOT_FOUND) {
        throw new CliError(CODES.NOT_FOUND, `No menu found for restaurant "${slug}". Use the slug from search output.`, {
          provider: name,
        });
      }
      throw err;
    }
  }

  async function fetchItems(manifest) {
    if (!manifest?.ItemsUrl) {
      throw new CliError(CODES.PARSE_ERROR, 'Menu manifest is missing its items reference.', { provider: name });
    }
    const doc = await http.getJson(`${MENU_CDN_BASE}/${manifest.ItemsUrl}`);
    return doc?.Items ?? [];
  }

  async function fetchItemDetails(manifest) {
    if (!manifest?.ItemDetailsUrl) return { ModifierGroups: [], ModifierSets: [] };
    return http.getJson(`${MENU_CDN_BASE}/${manifest.ItemDetailsUrl}`);
  }

  function menuCategories(manifest) {
    return (manifest?.Menus ?? []).flatMap((m) => m?.Categories ?? []);
  }

  return {
    name,

    async searchRestaurants(loc, { query = null, limit = 25, openNow = false } = {}) {
      const { restaurants } = await fetchDiscovery(loc);
      let list = restaurants;
      if (openNow) list = list.filter((r) => r.open.delivery || r.open.pickup);
      if (query) {
        const q = query.toLowerCase();
        list = list.filter(
          (r) =>
            (r.name ?? '').toLowerCase().includes(q) || r.cuisines.some((c) => String(c).toLowerCase().includes(q))
        );
      }
      list = [...list].sort((a, b) => (a.distance_m ?? Infinity) - (b.distance_m ?? Infinity));
      const total = list.length;
      if (limit > 0) list = list.slice(0, limit);
      return {
        location: { postcode: loc.postcode },
        total_matches: total,
        returned: list.length,
        restaurants: list,
      };
    },

    async getRestaurant(idOrSlug, loc = null) {
      // With a location, serve the full location-aware record from discovery.
      if (loc?.postcode) {
        const { restaurants } = await fetchDiscovery(loc);
        const hit = restaurants.find((r) => r.slug === idOrSlug || String(r.id) === String(idOrSlug));
        if (!hit) {
          throw new CliError(CODES.NOT_FOUND, `Restaurant "${idOrSlug}" does not deliver to ${loc.postcode} (or does not exist).`, {
            provider: name,
          });
        }
        return hit;
      }
      // Without a location, fall back to the menu manifest's static info.
      const manifest = await fetchManifest(idOrSlug);
      const info = manifest?.RestaurantInfo ?? {};
      return {
        id: manifest?.RestaurantId ?? null,
        slug: info?.SeoName ?? idOrSlug,
        name: info?.Name ?? null,
        address: {
          city: info?.Location?.City ?? null,
          street: info?.Location?.Address ?? null,
          postcode: info?.Location?.PostCode ?? null,
        },
        open: { delivery: null, pickup: null },
        delivery: { fee_cents: null, min_order_cents: null, eta_min: null, eta_max: null },
        note: 'Delivery fee, minimum order, ETA, and open state depend on the delivery location. Pass --postcode or --address for them.',
      };
    },

    async getMenu(idOrSlug, { category = null, includeOptions = false } = {}) {
      const manifest = await fetchManifest(idOrSlug);
      const items = await fetchItems(manifest);
      const details = includeOptions ? await fetchItemDetails(manifest) : null;
      const itemsById = new Map(items.map((i) => [String(i.Id), i]));

      let categories = menuCategories(manifest).map((c) => ({
        id: c?.Id ?? null,
        name: c?.Name ?? null,
        items: (c?.ItemIds ?? [])
          .map((iid) => itemsById.get(String(iid)))
          .filter(Boolean)
          .map((i) => normalizeItem(i, { details })),
      }));
      if (category) {
        const q = String(category).toLowerCase();
        categories = categories.filter((c) => String(c.id).toLowerCase() === q || (c.name ?? '').toLowerCase().includes(q));
        if (categories.length === 0) {
          throw new CliError(CODES.NOT_FOUND, `No menu category matches "${category}".`, { provider: name });
        }
      }
      return {
        restaurant_slug: idOrSlug,
        restaurant_name: manifest?.RestaurantInfo?.Name ?? null,
        currency: 'EUR',
        category_count: categories.length,
        item_count: categories.reduce((n, c) => n + c.items.length, 0),
        categories,
      };
    },

    async getItem(idOrSlug, itemId) {
      if (!itemId) {
        throw new CliError(CODES.INVALID_ARGUMENT, 'An item id is required.', { provider: name, exitCode: 2 });
      }
      const manifest = await fetchManifest(idOrSlug);
      const items = await fetchItems(manifest);
      const item = items.find((i) => String(i.Id) === String(itemId));
      if (!item) {
        throw new CliError(CODES.NOT_FOUND, `Item ${itemId} not found in ${idOrSlug}'s menu.`, { provider: name });
      }
      const details = await fetchItemDetails(manifest);
      return {
        restaurant_slug: idOrSlug,
        currency: 'EUR',
        item: normalizeItem(item, { details }),
      };
    },

    async availability(loc) {
      const { restaurants, meta } = await fetchDiscovery(loc);
      const openDelivery = restaurants.filter((r) => r.open.delivery === true).length;
      const openPickup = restaurants.filter((r) => r.open.pickup === true).length;
      return {
        location: {
          postcode: loc.postcode,
          area: meta?.area ?? null,
        },
        restaurant_count: restaurants.length,
        open_for_delivery: openDelivery,
        open_for_pickup: openPickup,
        closed: restaurants.filter((r) => r.open.delivery === false && r.open.pickup === false).length,
        deliverable: openDelivery > 0,
      };
    },
  };
}
