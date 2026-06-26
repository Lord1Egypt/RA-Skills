---
name: mcdonalds-mcp-order-lite
description: Place McDonald's China delivery orders through the official MCP server at https://mcp.mcd.cn using a Bearer MCP token over Streamable HTTP / JSON-RPC. Use when the user wants to browse McDonald's deliverable addresses, query store menu items, inspect meal details, calculate price, create a delivery order, query order status, or check McDonald's coupons/points. Also use when wiring this MCP into a client like Cursor, Cherry Studio, Trae, or another agent. This lite package intentionally contains no embedded token and only the core reusable files.
---

Use the official McDonald's China MCP toolchain, not scraped web APIs.

## Core workflow

1. Identify the delivery address.
2. Call `delivery-query-addresses` first.
3. Pick the matching address record and carry forward `addressId`, `storeCode`, and `beCode` from the same record.
4. Call `query-meals` for that store.
5. If needed, call `query-meal-detail` for a chosen meal code.
6. Call `calculate-price` before ordering.
7. Show the user the real payable amount and wait for confirmation.
8. Call `create-order` only after confirmation.
9. Return the `payH5Url` to the user.
10. After the user says payment is complete, call `query-order`.

## Important constraints

- Use server URL `https://mcp.mcd.cn`.
- Send `Authorization: Bearer <TOKEN>`.
- MCP protocol version must be `2025-06-18` or earlier.
- Prefer low request volume; the docs say 600 requests/minute/token.
- Do not invent `storeCode`, `beCode`, or `addressId`.
- For delivery ordering, always use values returned by `delivery-query-addresses` or `delivery-create-address`.
- Always price-check with `calculate-price` before `create-order`.
- `query-meal-detail` docs note that replacing default combo choices is not yet supported in current version.

## Tool map

### Delivery ordering
- `delivery-query-addresses`: list saved deliverable addresses
- `delivery-create-address`: add a new delivery address
- `query-store-coupons`: coupons usable for the chosen store
- `query-meals`: menu for the chosen store
- `query-meal-detail`: inspect a meal / combo
- `calculate-price`: final price check
- `create-order`: create payable delivery order
- `query-order`: query order status after creation/payment

### Other useful tools
- `available-coupons`: claimable coupons
- `auto-bind-coupons`: one-click claim current coupons
- `query-my-coupons`: coupon wallet
- `list-nutrition-foods`: nutrition list
- `query-my-account`: points account
- `mall-points-products`, `mall-product-detail`, `mall-create-order`: points mall
- `campaign-calendar`: marketing calendar
- `now-time-info`: server time

## Recommended user-facing flow

When the user says “帮我点麦当劳” or similar:

- Confirm budget / preferred item if missing.
- Resolve the delivery address from saved addresses first.
- Find candidate items from `query-meals`.
- Use `calculate-price` for one or a few concrete combinations.
- Present the cheapest / best-fit options with real payable totals.
- Only place the order after explicit confirmation.
- After order creation, send the payment link.
- After payment, query `query-order` instead of assuming success.

## Files in this skill

- Read `references/api.md` for the compact API cheat sheet and tested field names.
- Use `scripts/mcd_rpc.py` for direct RPC calls to the remote MCP server when you need deterministic testing or CLI usage.
- `client.py` contains a Python wrapper around the same remote MCP calls.
- `nlp_processor.py` contains lightweight text parsing for order intent.
- `tools.py` contains higher-level helper functions.

## Packaging notes

Keep the skill folder lean.
Do not add extra docs beyond what is needed for reuse.
Remove transient files like `__pycache__` before packaging.
