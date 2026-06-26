---
name: pet-me-master
description: Batch-pet Aavegotchis on Base via Bankr with cooldown checks, reminder automation, and natural-language routing.
homepage: https://github.com/aaigotchi/pet-me-master
metadata:
  openclaw:
    requires:
      bins:
        - cast
        - jq
        - curl
        - python3
      env:
        - BANKR_API_KEY
---

# Pet Me Master

Batch-only pet flow for Aavegotchis:
- Discovers gotchis owned by your agent wallet
- Adds gotchis delegated (lent) to your wallet from the Base core subgraph
- Checks cooldown on-chain (`lastInteracted`)
- Sends one `interact(uint256[])` tx through Bankr for all ready gotchis
- Sends reminder and fallback auto-pet if no reply

## Config

Create `~/.openclaw/workspace/skills/pet-me-master/config.json`:

```json
{
  "contractAddress": "0xA99c4B08201F2913Db8D28e71d020c4298F29dBF",
  "rpcUrl": "https://mainnet.base.org",
  "chainId": 8453,
  "walletAddress": "0xYourAgentWallet",
  "dailyReminder": true,
  "fallbackDelayHours": 1,
  "reminder": {
    "enabled": true,
    "telegramChatId": "YOUR_CHAT_ID",
    "fallbackDelayHours": 1
  }
}
```

Wallet resolution order:
1. `PET_ME_WALLET_ADDRESS` / `BANKR_WALLET_ADDRESS`
2. `config.walletAddress` / `config.wallet`
3. Bankr prompt: `What is my Base wallet address?`

Reminder chat resolution order:
1. `PET_ME_TELEGRAM_CHAT_ID`
2. `TELEGRAM_CHAT_ID`
3. `config.reminder.telegramChatId` (or `config.telegramChatId`)

## Bankr Auth

This skill submits transactions directly to Bankr API and resolves API key from:
1. `BANKR_API_KEY` env
2. `systemctl --user` exported environment
3. `~/.openclaw/skills/bankr/config.json` (`apiKey`)
4. `~/.openclaw/workspace/skills/bankr/config.json` (`apiKey`)

## Scripts

- `./scripts/check-cooldown.sh [gotchi-id]`
- `./scripts/pet-all.sh [--dry-run]`
  - Discover owned + delegated gotchis, then batch-pet ready ones
- `./scripts/pet.sh [--dry-run]`
  - Batch-only wrapper to `pet-all.sh`
- `./scripts/pet-status.sh`
  - Shows status for discovered owned + delegated gotchis
- `./scripts/check-status.sh`
  - Wrapper for `pet-status.sh`
- `./scripts/pet-command.sh [--dry-run] [--tx-dry-run] "<natural-language command>"`
  - Any pet action routes to batch mode
- `./scripts/check-and-remind.sh`
- `./scripts/auto-pet-fallback.sh`
- `./scripts/auto-pet-at-cooldown.sh`
  - Waits until all discovered owned+delegated gotchis are ready (re-check loop for desync), then runs batch pet and sends Telegram with total count + petted IDs
- `./scripts/schedule-dynamic-check.sh`

## Natural-Language Routing

Examples:

```bash
./scripts/pet-command.sh "pet my gotchis"
./scripts/pet-command.sh "pet all my gotchis"
./scripts/pet-command.sh "pet status"
./scripts/pet-command.sh "check cooldown for gotchi 9638"
```

## Operational Notes

- Cooldown threshold is `43260` seconds (12h + 1m).
- Reminder trigger is when all discovered gotchis are ready.
- If no user action, fallback runs after configured delay (default 1 hour).
- Fallback and manual pet both use batch flow.

## Troubleshooting

- `Could not resolve agent wallet address`
  - Set `PET_ME_WALLET_ADDRESS` or `config.walletAddress`.
- `BANKR_API_KEY is missing`
  - Export `BANKR_API_KEY` or configure Bankr skill API key.
- `Telegram chat ID missing`
  - Set `PET_ME_TELEGRAM_CHAT_ID` or `config.reminder.telegramChatId`.
- Cooldown checks fail
  - Verify `rpcUrl`, contract address, and Base RPC connectivity.
