# Gotchi Channeling

Automate Aavegotchi Alchemica channeling on Base via Bankr wallet submission.

## Scripts

- `./scripts/check-cooldown.sh <gotchi-id>`
  - Returns `ready:0` or `waiting:<seconds>`
- `./scripts/channel.sh <gotchi-id> <parcel-id>`
  - Channels one gotchi if cooldown is ready
- `./scripts/channel-all.sh`
  - Reads `config.json` and channels all ready entries

## Requirements

- `cast` (Foundry)
- `jq`
- `curl`
- Bankr API key

Bankr API key resolution order:
1. `BANKR_API_KEY`
2. user systemd environment (`systemctl --user show-environment`)
3. `~/.openclaw/skills/bankr/config.json`
4. `~/.openclaw/workspace/skills/bankr/config.json`

## Config

Default config path: `./config.json`
Override path: `GOTCHI_CHANNELING_CONFIG_FILE=/path/to/config.json`

Example:

```json
{
  "realmDiamond": "0x4B0040c3646D3c44B8a28Ad7055cfCF536c05372",
  "rpcUrl": "https://mainnet.base.org",
  "chainId": 8453,
  "channeling": [
    {
      "parcelId": "867",
      "gotchiId": "9638",
      "description": "Primary pair"
    }
  ]
}
```

## Notes

- Cooldown is 24h (`86400` seconds).
- `channel.sh` fails closed if cooldown/RPC checks fail.
- `channel-all.sh --help` is non-destructive.
