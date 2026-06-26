---
name: gotchi-dao-voting
description: Check active Aavegotchi DAO proposals and vote on Snapshot via Bankr EIP-712 signatures.
homepage: https://github.com/aaigotchi/gotchi-dao-voting
metadata:
  openclaw:
    requires:
      bins:
        - curl
        - jq
      env:
        - BANKR_API_KEY
---

# gotchi-dao-voting

Vote on Snapshot proposals for `aavegotchi.eth`.

## Scripts

- `./scripts/list-proposals.sh`
  - Lists active proposals and your VP per proposal.
- `./scripts/vote.sh [--dry-run] <proposal-id> <choice>`
  - Submits signed vote through Snapshot sequencer.
  - `--dry-run` prints typed data and exits without signing/submitting.

## Choice Formats

- Single-choice proposal: numeric option, e.g. `2`
- Weighted proposal: JSON object string, e.g. `'{"2":2238}'`
  - If you pass just `2` for a weighted vote, script auto-converts to `{"2":<floor(vp)>}`.

## Config

`config.json` keys:
- `wallet`
- `space`
- `snapshotApiUrl`
- `snapshotSequencer`

## Security

- Uses Bankr signing API (no local private key usage).
- Off-chain Snapshot voting (no gas transaction).
- Input validation for proposal ID, wallet, choice format, and choice range.
