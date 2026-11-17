// Provider contract. Every food-delivery provider implements this shape so the
// CLI layer stays provider-agnostic and Uber Eats (or others) can be added
// without touching command handling. See docs/adding-uber-eats.md.
//
// All methods are READ-ONLY: they must never place orders, mutate carts on the
// platform, authenticate a user, or touch payment. Cart simulation is handled
// locally by the CLI layer using data returned from these methods.
//
// /**
//  * @typedef {object} Provider
//  * @property {string} name                      e.g. "lieferando"
//  * @property {(loc, opts) => Promise<object>} searchRestaurants
//  *     loc: {postcode, lat, lng}; opts: {query?, limit?, openNow?}
//  *     -> { location, count, restaurants: NormalizedRestaurant[] }
//  * @property {(idOrSlug, loc?) => Promise<object>} getRestaurant
//  *     -> NormalizedRestaurantDetail (info, delivery fees, opening state)
//  * @property {(idOrSlug, opts?) => Promise<object>} getMenu
//  *     -> { restaurant_id, currency, categories: [{id, name, items: NormalizedItem[]}] }
//  * @property {(idOrSlug, itemId) => Promise<object>} getItem
//  *     -> NormalizedItem with option_groups fully expanded
//  * @property {(loc) => Promise<object>} availability
//  *     -> { location, deliverable, open_count, closed_count, restaurant_count }
//  */
//
// Normalized shapes (all prices in minor units, i.e. euro cents):
//   NormalizedRestaurant: { id, slug, name, cuisines[], rating: {score, votes},
//     open: {delivery, pickup}, delivery: {fee_min_cents, duration_min, min_order_cents}, distance_m }
//   NormalizedItem: { id, name, description, price_cents, currency,
//     option_group_ids[] or option_groups[] }

export const PROVIDER_METHODS = ['searchRestaurants', 'getRestaurant', 'getMenu', 'getItem', 'availability'];

/** Sanity-check a provider object implements the contract. */
export function assertProvider(p) {
  for (const m of PROVIDER_METHODS) {
    if (typeof p[m] !== 'function') throw new Error(`Provider ${p?.name ?? '?'} missing method ${m}`);
  }
  if (!p.name) throw new Error('Provider must have a name');
  return p;
}
