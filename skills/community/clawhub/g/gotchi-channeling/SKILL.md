---
name: gotchi-channeling
description: Channel Aavegotchis on Base via Bankr. Checks cooldown, builds calldata, and submits channel txs safely.
homepage: https://github.com/aaigotchi/gotchi-channeling
metadata:
  openclaw:
    requires:
      bins:
        - cast
        - jq
        - curl
      env:
        - BANKR_API_KEY
    primaryEnv: BANKR_API_KEY
---

# gotchi-channeling

Channel Alchemica for configured gotchi/parcel pairs.

## Scripts

- `./scripts/check-cooldown.sh <gotchi-id>`
  - Outputs `ready:0` or `waiting:<seconds>`.
  - Fails if RPC query fails.
- `./scripts/channel.sh <gotchi-id> <parcel-id>`
  - Validates cooldown, submits tx via Bankr, prints tx hash.
- `./scripts/channel-all.sh`
  - Iterates `config.json` pairs and channels only ready gotchis.

## Config

`config.json` keys:
- `realmDiamond`
- `rpcUrl`
- `chainId`
- `channeling[]` entries: `{ "parcelId": "...", "gotchiId": "...", "description": "..." }`

Optional env:
- `GOTCHI_CHANNELING_CONFIG_FILE` override config path.
- `BASE_MAINNET_RPC` overrides `rpcUrl`.

## Bankr API key resolution

1. `BANKR_API_KEY`
2. `systemctl --user show-environment`
3. `~/.openclaw/skills/bankr/config.json`
4. `~/.openclaw/workspace/skills/bankr/config.json`

## Quick use

```bash
./scripts/check-cooldown.sh 9638
./scripts/channel.sh 9638 867
./scripts/channel-all.sh
```

## Safety notes

- Cooldown enforced at 24h (`86400` seconds).
- Scripts fail closed on RPC/config/tool errors.
- Batch mode exits non-zero when any entry fails.
