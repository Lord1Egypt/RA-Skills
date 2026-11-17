// LOCAL cart simulation. Nothing here talks to the platform's basket,
// checkout, or payment systems. The cart is a JSON file on disk; "preview"
// is arithmetic over prices already fetched via read-only menu endpoints.
// Every payload is stamped simulation:true so agents cannot mistake it for a
// real order flow.

import { readFileSync, writeFileSync, mkdirSync, rmSync } from 'node:fs';
import { join } from 'node:path';
import { homedir } from 'node:os';
import { CliError, CODES } from './errors.js';

function stateDir() {
  return process.env.LIEFERANDO_CLI_STATE_DIR || join(homedir(), '.local', 'state', 'lieferando-cli');
}

function cartPath() {
  return join(stateDir(), 'cart.json');
}

export function loadCart() {
  try {
    return JSON.parse(readFileSync(cartPath(), 'utf8'));
  } catch {
    return null;
  }
}

function saveCart(cart) {
  mkdirSync(stateDir(), { recursive: true });
  writeFileSync(cartPath(), JSON.stringify(cart, null, 2));
}

export function clearCart() {
  try {
    rmSync(cartPath());
  } catch {
    // already empty
  }
}

/**
 * Validate an item + options selection against the live menu and add it to the
 * local cart. `provider.getItem` is the only network call and is read-only.
 */
export async function cartAdd(provider, { restaurant, itemId, variantId = null, count = 1, options = {} }) {
  if (!restaurant || !itemId) {
    throw new CliError(CODES.INVALID_ARGUMENT, 'cart add needs --restaurant <slug> and --item <id>.', { exitCode: 2 });
  }
  if (!Number.isInteger(count) || count < 1 || count > 20) {
    throw new CliError(CODES.INVALID_ARGUMENT, '--count must be an integer between 1 and 20.', { exitCode: 2 });
  }

  const existing = loadCart();
  if (existing && existing.restaurant_slug !== restaurant) {
    throw new CliError(
      CODES.CART_ERROR,
      `Cart already holds items from "${existing.restaurant_slug}". Run "cart clear" first.`,
      { provider: provider.name }
    );
  }

  const { item, currency } = await provider.getItem(restaurant, itemId);
  const variants = item.variants ?? [];
  const variant = variantId ? variants.find((v) => String(v.id) === String(variantId)) : variants[0];
  if (!variant) {
    throw new CliError(CODES.NOT_FOUND, `Variant ${variantId ?? '(default)'} not found for item ${itemId}.`, {
      provider: provider.name,
    });
  }

  // Validate selected options against the item's option groups.
  const selected = [];
  const groupsById = new Map((variant.option_groups ?? []).map((g) => [String(g.id), g]));
  for (const [gid, optionIds] of Object.entries(options)) {
    const group = groupsById.get(String(gid));
    if (!group) {
      throw new CliError(CODES.CART_ERROR, `Option group ${gid} does not belong to item ${itemId}.`, {
        provider: provider.name,
      });
    }
    const ids = Array.isArray(optionIds) ? optionIds : [optionIds];
    for (const oid of ids) {
      const opt = (group.options ?? []).find((o) => String(o.id) === String(oid));
      if (!opt) {
        throw new CliError(CODES.CART_ERROR, `Option ${oid} not found in group ${gid} ("${group.name}").`, {
          provider: provider.name,
        });
      }
      selected.push({
        group_id: gid,
        group_name: group.name,
        option_id: oid,
        option_name: opt.name,
        price_cents: opt.price_cents ?? 0,
      });
    }
  }
  // Enforce min_choices for required groups the caller did not fill.
  for (const g of groupsById.values()) {
    const chosen = selected.filter((s) => String(s.group_id) === String(g.id)).length;
    if ((g.min_choices ?? 0) > chosen) {
      throw new CliError(
        CODES.CART_ERROR,
        `Option group "${g.name}" (${g.id}) requires at least ${g.min_choices} choice(s). Pass --options '{"${g.id}": ["<option-id>"]}'.`,
        { provider: provider.name }
      );
    }
  }

  const unit = (variant.price_cents ?? 0) + selected.reduce((n, s) => n + (s.price_cents ?? 0), 0);
  const line = {
    item_id: itemId,
    item_name: item.name,
    variant_id: variant.id,
    variant_name: variant.name,
    count,
    options: selected,
    unit_price_cents: unit,
    line_total_cents: unit * count,
  };

  const cart = existing ?? {
    simulation: true,
    provider: provider.name,
    restaurant_slug: restaurant,
    currency,
    lines: [],
  };
  cart.lines.push(line);
  saveCart(cart);
  return cartSummary(cart);
}

export function cartSummary(cart) {
  if (!cart) return { simulation: true, empty: true, lines: [], subtotal_cents: 0 };
  const subtotal = cart.lines.reduce((n, l) => n + l.line_total_cents, 0);
  return { ...cart, simulation: true, empty: cart.lines.length === 0, subtotal_cents: subtotal };
}

/**
 * Compute a checkout-style preview LOCALLY: subtotal from the cart file plus
 * delivery fee / minimum-order data from the read-only restaurant endpoint.
 * No basket is created on the platform; nothing can be submitted from here.
 */
export async function cartPreview(provider, loc = null) {
  const cart = loadCart();
  if (!cart || cart.lines.length === 0) {
    throw new CliError(CODES.CART_ERROR, 'Local cart is empty. Add items with "cart add" first.', {
      provider: provider.name,
    });
  }
  const info = await provider.getRestaurant(cart.restaurant_slug, loc);
  const subtotal = cart.lines.reduce((n, l) => n + l.line_total_cents, 0);
  const deliveryFee = info.delivery?.fee_cents ?? null;
  const minOrder = info.delivery?.min_order_cents ?? null;
  return {
    simulation: true,
    note: 'Locally computed preview. No basket was created on the platform and no order can be placed with this tool.',
    provider: provider.name,
    restaurant: { slug: cart.restaurant_slug, name: info.name, open_for_delivery: info.open?.delivery ?? null },
    currency: cart.currency,
    lines: cart.lines,
    subtotal_cents: subtotal,
    delivery_fee_cents: deliveryFee,
    min_order_cents: minOrder,
    min_order_met: minOrder != null ? subtotal >= minOrder : null,
    estimated_total_cents: deliveryFee != null ? subtotal + deliveryFee : subtotal,
    estimated_delivery_min: info.delivery?.eta_min ?? null,
  };
}
