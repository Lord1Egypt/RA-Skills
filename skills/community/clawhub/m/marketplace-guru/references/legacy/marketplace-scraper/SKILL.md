---
name: marketplace-scraper
description: Search and compare product prices across Russian marketplaces (Яндекс Маркет, Ozon, Wildberries) using a visible Windows browser. Use when you need to find the best price, availability, or delivery option for a product. Requires the `win11-visible-browser` skill.
metadata: {"openclaw":{"requires":{"skills":["win11-visible-browser"]}}}
---

# Marketplace Scraper

Search, compare, and report product prices across Russian marketplaces using the visible Windows browser.

## Requirements

- The `win11-visible-browser` skill must be installed and configured:
  - OpenClaw browser profile `win-edge` connected to a visible Windows browser via CDP.
  - See `win11-visible-browser/references/setup.md` for setup details.
  - Browser repair/doctor scripts in `win11-visible-browser/scripts/`.

## When to use

- Find the best price for a specific product across marketplaces.
- Check availability and delivery speed in Moscow.
- Compare specifications between product variants.
- The task already needs a visible browser (login, captcha, manual takeover).

## Layered search strategy

Use the lightest tool that works. Escalate only when blocked.

1. **web_search** (DuckDuckGo) — first pass: 1–2 seconds, low tokens.
   - Gives structured snippets with price, availability, seller, link.
   - Good enough for the question "what exists and roughly for how much?".
2. **web_fetch** — depth pass: cheap, ~1 second.
   - Extracts product page text/details when the site allows it.
   - Falls on captcha sites (Ozon, WB, М.Видео).
3. **visible browser** (via win11-visible-browser) — final escalation: slow but reliable.
   - Needed for captcha-protected pages, JS-heavy rendering, exact stock/price confirmation.
   - Use `evaluate` for bulk extraction, not repeated snapshots.

Overcoming blocks:
- If web_search returns nothing useful — skip to browser.
- If web_fetch returns captcha/antibot — escalate to browser.
- If the browser shows a captcha — report to the user; do not retry in a loop.
- If the page blocks automated access but works visibly — the CDP-attached browser usually passes.

## Procedure

1. Search with the lightest layer that works for the target site (see above).
2. For the browser layer: open the marketplace search URL in a tab.
3. Confirm results loaded; snapshot or evaluate to verify.
4. Extract all visible product cards in a single `act kind=evaluate` call:
   - name, price (current and original), seller/merchant, delivery date range, product link.
5. Repeat for each remaining marketplace (new tab or same tab).
6. Present a concise comparison — no fluff, just the data the user needs to decide.

For pagination or lazy-loaded content, scroll into view and re-extract with evaluate;
no new snapshot needed unless the DOM structure fundamentally changes.

## Supported marketplaces

| Marketplace | Search URL pattern | Notes |
|---|---|---|
| Яндекс Маркет | `https://market.yandex.ru/search?text={query}` | Works with `web_fetch` and visible browser. |
| Ozon | `https://www.ozon.ru/search/?text={query}` | May show antibot; use visible browser. |
| Wildberries | `https://www.wildberries.ru/catalog/0/search.aspx?search={query}` | May show antibot; use visible browser. |
| М.Видео | `https://www.mvideo.ru/search/?q={query}` | May show antibot; check availability per-store. |
| Ситилинк | `https://www.citilink.ru/search/?text={query}` | Generally works with fetch. |
| DNS | `https://www.dns-shop.ru/search/?q={query}` | Generally works with fetch. |

## Safety

- Read-only. No purchases, no account login, no form submission.
- If a marketplace requires captcha or manual intervention — report to the user, do not loop.
- The underlying `win11-visible-browser` skills safety gate still applies: state-changing actions require explicit confirmation.

## Known limitations

- Prices fluctuate; data is valid at extraction time.
- Wildberries shows prices excluding WB Кошелёк discounts; final price may differ.
- Ozon may show "цена с банками" which requires a specific card.
- Some marketplace APIs (Ozon, WB) block `web_fetch` and need the visible CDP browser.

## Example

User: "Найди ADATA Legend 960 2TB на Яндекс Маркете, Ozon и WB"

1. Search Яндекс Маркет, extract prices/sellers/delivery.
2. Search Ozon via visible browser, extract.
3. Search WB via visible browser, extract.
4. Present table with prices, availability, delivery, links.
