# Marketplace Guru

Marketplace Guru is an **OpenClaw skill** for disciplined marketplace product search, price comparison, risk checks, and decision-ready purchase recommendations.

It is a read-only purchasing advisor: it compares options and gives decision-ready recommendations, but does not buy, add to cart, or change accounts.

Marketplace Guru is region-aware. It can work with global marketplaces and local retail ecosystems: Amazon, eBay, AliExpress, brand stores, specialty retailers, and regional marketplaces such as Ozon, Wildberries, and Яндекс Маркет when the delivery region makes them relevant.

## Requirements

- OpenClaw tools for web search/fetch.
- Optional: browser automation for JS-heavy marketplaces and exact price/delivery checks.
- Optional: a visible/logged-in browser profile when local marketplace prices, delivery slots, or account-specific discounts require it.

## Setup

No API keys are required for the MVP.

For best results, configure browser access for the marketplaces you use most. Browser access helps the agent inspect pages that require real rendering, region selection, seller details, recommendations, and delivery estimates.

## Usage

Examples:

- “Find the best price for this exact product link and check promo codes.”
- “Compare robot vacuums under $400 with fast delivery to Berlin.”
- “I need a Zigbee USB coordinator for Home Assistant; cheapest is fine, I can wait.”
- “Is this SSD worth buying, or are there better alternatives?”
- “Подбери Zigbee USB coordinator для Home Assistant, дешевле, можно ждать.”
- “Сравни эту сыворотку на Ozon, Wildberries и Яндекс Маркете.”

## Behavior

Marketplace Guru first asks only what matters:

- where delivery is needed;
- whether the user wants a specific model or alternatives are allowed;
- 1–2 key criteria such as budget, deadline, reliability, size, compatibility, or warranty.

Then it searches and returns a short decision-oriented recommendation:

- best overall;
- value option;
- reliable/premium option;
- fastest delivery when relevant;
- avoid/risky options.

## Source planning

The skill chooses sources by both category and purchase mode:

- urgent/local purchase → local marketplaces and retailers first;
- cheapest / willing to wait → global marketplaces and direct sellers included;
- DIY / open firmware / experimental hardware → compatibility docs plus global/direct sources;
- warranty/reliability → official stores and reputable local retailers;
- exact model/SKU/link → verify the exact item first, then compare sellers and regions.

## Safety

- No purchases.
- No cart actions.
- No payment handling.
- No account changes.
- Captchas/login walls are reported, not bypassed.

## Install

```bash
clawhub install Pe4atnik/marketplace-guru
```
