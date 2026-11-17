const CURRENCY_SYMBOL = '¥';

/**
 * Single source of truth for money display.
 * Never hardcode a currency symbol in a component — always go through this helper.
 * The locale only controls digit grouping; keep it aligned with the target market.
 */
export function formatPrice(value: number): string {
  return `${CURRENCY_SYMBOL}${Math.round(value).toLocaleString('en-US')}`;
}

/** Free-shipping threshold used by CartDrawer, ProductPage and CheckoutPage. */
export const FREE_SHIPPING_THRESHOLD = 299;
