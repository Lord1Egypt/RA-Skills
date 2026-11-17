# lyra-crypto-operator

**Canonical home** for LYRA / Clawnch token launch utilities — **not** part of LYGO P0–P9 lattice verification.

| Skill (ClawHub slug) | Role |
|----------------------|------|
| `lyra-coin-launch-manager` | Clawnch receipts, Starcore family normalize/verify, bookmarks |

## Policy

Read `CRYPTO_LATTICE_SEPARATION.md`. Token metrics ≠ `lattice.ok`. Install only when you explicitly run launches.

## Wallet / keys (read this before LYRA autonomy tests)

**This repo does not hold private keys.** Scripts only call the public Clawnch API and read/write **local JSON** under `state/` (gitignored).

| Do | Don't |
|----|--------|
| Keep deployer wallet / mnemonic **outside** this repo (e.g. `I:\E Drive\…` vault, password manager, hardware wallet) | Never commit `.env`, `wallet*.json`, mnemonics, or `0x…` 64-char private keys |
| Run `python scripts/scan_for_secrets.py --all` before push | Don't let agents write key material into this tree |

```powershell
python scripts/scan_for_secrets.py --install-hook   # optional pre-commit
python scripts/push_github_auto.py                  # push (after scan in hook)
```

Real wallet autonomy tooling, if any, lives **elsewhere on your machine** — audit that path separately.

## Maintainer

```bash
# From this repo root
npx clawhub@latest publish . --slug lyra-coin-launch-manager --name "LYRA Coin Launch Manager"
```

## Stack bridge

`lygo-protocol-stack` keeps a **publish stub** at `clawhub/mirrors/lyra-coin-launch-manager/` synced from here via:

```powershell
python tools/sync_from_lyra_crypto_operator.py   # run from lygo-protocol-stack
```

**Δ9Φ963 — crypto operator lane, sovereign stack lane.**