# Gotchi DAO Voting

Snapshot voting automation for Aavegotchi DAO (`aavegotchi.eth`) using Bankr signing.

## Scripts

- `./scripts/list-proposals.sh`
  - Lists active proposals + your current VP for each
- `./scripts/vote.sh [--dry-run] <proposal-id> <choice>`
  - Single choice: `2`
  - Weighted choice: `'{"2":2238}'`

## Quick Start

```bash
# 1) List active proposals
./scripts/list-proposals.sh

# 2) Preview typed vote payload (safe)
./scripts/vote.sh --dry-run <proposal-id> 2

# 3) Submit vote
./scripts/vote.sh <proposal-id> 2
```

## Requirements

- `curl`, `jq`
- `BANKR_API_KEY` (env recommended)

Bankr API key resolution order:
1. `BANKR_API_KEY`
2. user systemd environment (`systemctl --user show-environment`)
3. `~/.openclaw/skills/bankr/config.json`
4. `~/.openclaw/workspace/skills/bankr/config.json`

## Config

`config.json`:

```json
{
  "wallet": "0xYourBankrWallet",
  "space": "aavegotchi.eth",
  "snapshotApiUrl": "https://hub.snapshot.org/graphql",
  "snapshotSequencer": "https://seq.snapshot.org/"
}
```

## Notes

- Snapshot voting is off-chain (no gas fee).
- Voting still requires correct VP at proposal snapshot block.
- `--dry-run` builds typed data without signing/submitting.
