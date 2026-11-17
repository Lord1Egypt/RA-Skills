---
name: lieferando-cli
description: "Read-only German food-delivery discovery for Lieferando (default) and Uber Eats: search restaurants near an address, inspect menus, item option groups, prices, delivery fees, ETA, and opening state. JSON envelope output. Cannot log in, order, or pay. Trigger when asked to find food, compare delivery options, or resolve menu/item details on Lieferando or Uber Eats in Germany."
homepage: https://clawhub.ai/skills/lieferando-cli
metadata: { "openclaw": { "emoji": "🥨", "requires": { "bins": ["node"] } } }
---

# Lieferando CLI

Read-only discovery for Lieferando (Just Eat Takeaway) in Germany. The tool is bundled with this skill (zero-dependency Node, needs Node >= 20). Every command prints one JSON envelope: `{ meta, data, warnings, error? }`.

```bash
node {baseDir}/scripts/lieferando.mjs <command> [flags]
```

All examples below use `lieferando-cli` as shorthand for that invocation.

## Hard Limits (tell the user, do not work around)

- This tool CANNOT place orders, log in, or touch payment. There is no such command.
- `cart` commands are a LOCAL simulation (`data.simulation: true`); nothing is sent to the platform.
- If you get `LFD_BLOCKED` or `LFD_RATE_LIMITED`, back off. Never retry in a tight loop, never attempt to bypass bot protection.
- Ordering itself must be done by the user in the Lieferando app/website. Hand them the restaurant slug and item names.

## Location Rules

- Pass `--address "Torstraße 1, 10119 Berlin"` (geocoded via OSM, needs street + postcode or city) OR `--postcode 10115` directly.
- Never combine `--address` with `--postcode/--lat/--lng`.
- German 5-digit postcodes only; primary target is Berlin/Germany.

## Providers

- Default: `lieferando`. Add `--provider ubereats` for Uber Eats Germany.
- Uber Eats specifics: restaurant/store ids are UUIDs from search output (`data.restaurants[].id`); the feed only lists currently open stores; `min_order_cents` is not exposed; item ids from promo carousels rotate, so on `LFD_NOT_FOUND` re-run `menu` and pick a fresh id from a canonical category; `--include-options` is not supported on `menu` (use `item`).
- Uber Eats `item` (option-group detail) hits their most protected endpoint. If it returns `LFD_BLOCKED`, stop using that command for at least an hour; `search`, `restaurant`, and `menu` (which already include item prices) keep working.

## Command Selection

- Find restaurants: `lieferando-cli search --postcode 10115 --query "pizza" --open-now --limit 10 --json`
- Delivery coverage summary: `lieferando-cli availability --postcode 10115 --json`
- One restaurant (fees, min order, ETA, open state): `lieferando-cli restaurant <slug> --postcode NNNNN --json` (without a location only static info is returned)
- Full menu: `lieferando-cli menu <slug> --json` (add `--category "pizza"` to narrow, `--include-options` for option groups inline)
- One item with option groups + prices: `lieferando-cli item <slug> <item-id> --json` (item ids are UUIDs from menu output)
- Local price simulation: `cart add --restaurant <slug> --item <id> [--variant <id>] [--count N] [--options '{"<group-id>":["<option-id>"]}']`, then `cart preview --postcode NNNNN --json`

Prefer `menu --category` over dumping full menus of large restaurants. Slugs come from `search` output (`data.restaurants[].slug`).

## Output Parsing

- Read payload from `.data`; surface `.warnings` to the user.
- All prices are integer euro cents (`*_cents`); divide by 100 for display.
- On failure `.error` = `{ code, message, provider, retryable }` and exit code is 1 (2 for usage errors).
- Retry (once, after a pause) only when `error.retryable` is true.

## Error Codes

`LFD_INVALID_ARGUMENT`, `LFD_GEOCODE_ERROR`, `LFD_NOT_FOUND`, `LFD_RATE_LIMITED` (retryable), `LFD_UPSTREAM_ERROR` (retryable if 5xx), `LFD_BLOCKED` (stop, do not retry), `LFD_NETWORK_ERROR` (retryable), `LFD_CART_ERROR`, `LFD_UNSUPPORTED_LOCATION`.

## Example Workflow

1. `lieferando-cli search --postcode 10115 --query sushi --open-now --json` → pick a slug by rating/fee/ETA.
2. `lieferando-cli menu <slug> --category maki --json` → pick item ids.
3. `lieferando-cli item <slug> <item-id> --json` (item ids are UUIDs from menu output) → resolve required option groups (`min_choices >= 1`).
4. Optionally simulate cost with `cart add` + `cart preview`.
5. Give the user the restaurant name, items, and estimated total; they order themselves.
