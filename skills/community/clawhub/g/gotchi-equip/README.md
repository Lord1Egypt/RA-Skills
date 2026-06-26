# gotchi-equip

Equip and manage wearables on your Aavegotchi NFTs on Base mainnet.

## Features

- Equip one or multiple slots in one transaction
- Preserves existing loadout when you update only selected slots
- Unequip all wearables
- View currently equipped items
- Secure Bankr transaction submission

## Quick Start

```bash
npm install

# Equip one slot (keeps all other slots unchanged)
./scripts/equip.sh 9638 right-hand=64

# Equip multiple slots
./scripts/equip.sh 9638 head=90 pet=151 right-hand=64

# Show equipped
./scripts/show-equipped.sh 9638

# Unequip all
./scripts/unequip-all.sh 9638
```

## Valid Slots

- `body`
- `face`
- `eyes`
- `head`
- `left-hand`
- `right-hand`
- `pet`
- `background`

## Requirements

- `node`
- `jq`
- `curl`
- Bankr API key

Bankr API key resolution order:
1. `BANKR_API_KEY`
2. user systemd environment (`systemctl --user show-environment`)
3. `~/.openclaw/skills/bankr/config.json`
4. `~/.openclaw/workspace/skills/bankr/config.json`
