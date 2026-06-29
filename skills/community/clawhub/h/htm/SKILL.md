---
name: htm
description: Fetch passes, products, and trips, and order new products from https://www.htm.nl 🇳🇱 "Mijn HTM" portal (Den Haag public transport)
metadata: {"clawdbot":{"emoji":"🇭","requires":{"bins":["node"],"env":["HTM_LOGIN","HTM_PASSWORD"]}}}
---
# Commands

```bash
node htm.mjs passes                                     # list passes (bank cards and OV-passen)
node htm.mjs products <tokenId>                          # products for a pass (active + inactive)
node htm.mjs reizen <tokenId> <from> <to>                            # trips for a pass, dates YYYY-MM-DD
node htm.mjs regio-advies <tokenId>[,<tokenId>...] <from> <to> [age] # is a Regio Vrij area pass worth it?
node htm.mjs reorder <tokenId> <productId> [validFrom]               # configure+cart a product, date YYYY-MM-DD
```

# Flow

Run `passes` first to get each pass's `id`. Use that `id` as `<tokenId>` for `products`, `reizen`,
`regio-advies`, and `reorder`.

`reizen` dates are local (Europe/Amsterdam) calendar dates, inclusive on both ends.

`regio-advies` checks, for each predefined "Regio Vrij" flat-rate area, whether a pass's actual
trip history in `<from>..<to>` would have covered enough fare per month to beat that area's
subscription price. A trip only counts as "covered" by an area if both its checkin and checkout
stop are members of that area. `age` is the age profile for pricing (`Adult` by default;
`Senior`/`Teenager`/`Child` also accepted) — it doesn't filter trips, only which price tier is used.
Pass multiple comma-separated `tokenId`s (e.g. to check every family member at once) and it
returns one result object per tokenId, in the same order.

`reorder` configures the given product (e.g. `5` = "HTM 20% Korting") for the pass and adds it to
the cart — it does **not** pay. It prints a `checkoutUrl` (`https://www.htm.nl/winkelwagen/`) to
open in a browser and finish payment manually (iDEAL etc. needs interactive bank authorization,
which can't be scripted). `validFrom` defaults to today; HTM rejects a start date more than ~30
days out with a clear error. Re-running `reorder` for the same pass+product reuses the same draft
line instead of creating a duplicate, so it's safe to call again to change the date.
