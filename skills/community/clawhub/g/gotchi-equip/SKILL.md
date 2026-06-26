---
name: gotchi-equip
description: Equip, unequip, and inspect Aavegotchi wearables on Base via Bankr submissions.
homepage: https://github.com/aaigotchi/gotchi-equip-skill
metadata:
  openclaw:
    requires:
      bins:
        - node
        - jq
        - curl
      env:
        - BANKR_API_KEY
      skills:
        - bankr
---

# gotchi-equip

Manage wearable loadouts for your gotchis.

## Scripts

- `./scripts/equip.sh <gotchi-id> <slot=wearableId> [slot=wearableId...]`
  - Updates selected slots while preserving existing equipped slots.
- `./scripts/unequip-all.sh <gotchi-id>`
  - Sets all 16 wearable slots to `0`.
- `./scripts/show-equipped.sh <gotchi-id>`
  - Shows currently equipped wearables from the Base subgraph.

## Slot names

`body`, `face`, `eyes`, `head`, `left-hand`, `right-hand`, `pet`, `background`

## Safety notes

- Gotchi ID is validated as numeric input.
- API key is resolved from env/systemd/bankr config paths.
- Equip flow fetches current loadout first to avoid accidental unequip of unspecified slots.
