# Styx Truncation Duplicate Fix

## Problem

Styx truncates merchant names to ~15 characters. The enrichment pipeline creates
separate items for each truncated variant instead of recognizing them as the same
restaurant via Google Places canonical name/address.

Examples found in production data (1,329 items, 60 duplicate groups, ~70 extra items):

- Milos Taverna / Milos Meze: `milostave`, `milos meze sa`, `milos meze` (3 items)
- Kasa Indian Eatery: 5 items across locations + Styx variants
- Little Star Pizza: `littlesta`, `little star pizza` (2 items)
- Chaat Corner / Chaatcorn: `chaatcorn`, `chaat corner` (2 items)
- Ike's Love & Sandwiches: `ikesloves`, `ikes`, `ike's love & sandwiches` (3 items)
- Freshroll: `freshroll`, `freshroll is confirmed` (2 items, 38 signals split)

## Root Cause

The dedup in styx_delta.md Step 2 only checks items.jsonl for name.lower().strip()
(the raw Styx merchant_name). It does NOT group truncated variants before
enrichment or dedup on Google Places canonical displayName after enrichment.

## Fix: Enrichment-Level Dedup

After querying Styx for merchant names, batch Google Places text search for ALL
unique names first. Group results by place_id (or canonical name + address).
Then create ONE ItemRecord per canonical venue with aggregated signals/spend
from all variant transactions.

## Fix: Signal-Item Linkage

CRITICAL: Styx-sourced signals have item_id=None. They use venue_name (raw
truncated Styx name) not item_id for linkage. The item-signal graph is broken.

After creating canonical items, update all signals to set item_id to the
canonical item_id where venue_name matches any variant.

## Cleanup Script

scripts/fix_styx_dedup.py handles the merge:
- Groups items by canonical name + address
- Merges signal counts, spend, visit dates
- Deduplicates signals by (item_id, date, source)
- Always run with --dry-run first

## Prevention

When writing enrichment scripts:
1. Always canonicalize first -- batch Places search, group by place_id
2. Dedup on place_id, not on raw merchant name
3. Set item_id on signals after canonicalization
4. Use UUID for item_id, signal_type: "purchase", domain: "food"

The bundled taste_full_enrich.py does NOT do this dedup and has schema drift
(item-{slug} instead of UUID, strength instead of signal_type).