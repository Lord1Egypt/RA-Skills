# Ticket Bot Starter Notes

Use this reference when adapting the bundled ticket bot starter.

## What It Includes

- slash command to deploy a ticket panel
- button-based ticket creation
- one-open-ticket-per-user enforcement
- SQLite persistence
- claim-ticket flow
- archive-based close flow
- reopen-ticket flow on the same channel
- transcript export to local files during archive
- attachment URL capture in transcripts

## Intended Scope

This starter is intentionally minimal. Extend it with:
- persistent guild config instead of raw env-only IDs
- stronger staff permission checks
- category/channel existence validation
- richer transcript support for embeds and edited/deleted content
- channel cleanup/retention policies
- companion API/dashboard if configuration should be edited outside Discord

## Safe Upgrade Path

1. move hardcoded env-based IDs into persistent guild config
2. add staff claim override or admin reclaim
3. improve transcript richness and retention policies
4. add dashboard/API integration if non-Discord config UX is needed
5. add logging/mod-log integration
6. add robust error handling and recovery
