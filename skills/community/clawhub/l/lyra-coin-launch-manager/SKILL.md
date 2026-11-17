---
name: lyra-coin-launch-manager
description: "Clawnch coin-launch receipts + local verify: pull launches from clawn.ch, write receipt JSON/MD, optional Blockscout/Dexscreener checks, local bookmark ref files. No git push, no GitHub token load, no repo create. Not for remote wallet control. Read references/SECURITY.md first."
version: 1.2.0
license: LYGO-Sovereign-v2.0
metadata:
  openclaw:
    emoji: "🪙"
    homepage: "https://github.com/DeepSeekOracle/lyra-crypto-operator"
    requires:
      anyBins: [python, python3]
  lyra: true
  lygo: false
  lattice: "crypto_lane_separated"
  signature: "Delta9Phi963-LYRA-COIN-LAUNCH-v1.2.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lyra-coin-launch-manager"
  security_audit: "skillspector-2026-07-29-v1.2.0"
  permissions_declared:
    filesystem: "cwd_state_and_reference_dirs_only"
    network: "https_get_clawnch_blockscout_dexscreener"
    process_spawn: false
    shell: false
    git_push: false
    github_token: false
    github_repo_create: false
    social_autopublish: false
---

# LYRA Coin Launch Manager v1.2.0

**Clawnch receipt + verification workflow only.**  
Crypto lane is **lattice-separated** from LYGO P0–P9 core (`CRYPTO_LATTICE_SEPARATION.md`). Token metrics ≠ lattice health.

## What this skill does

| Action | Network | Disk | Credentials |
|--------|---------|------|-------------|
| Pull launches from Clawnch API | HTTPS GET `clawn.ch` | Write `state/*_clawnch_receipt.json` | None |
| Normalize STARCORE family receipts | Optional Clawnch GET | Write state + `reference/*.md` | None |
| Verify via Blockscout / Dexscreener | HTTPS GET | Write `state/*_verify.json` | None |
| Local bookmark ref files | None | Write under `--bookmark-dir` | None |

## What this skill does **not** do

- **No** GitHub token load / `git push` / `gh repo create`  
- **No** git credential fill / pre-commit hook install  
- **No** wallet private keys / signing / transfers  
- **No** auto social posts (you post `!clawnch` yourself)  
- **No** LYGO stack mutation  

Operator-only publish helpers (if any) live outside this package in `operator_tools/` of the steward crypto repo — **not** shipped on ClawHub.

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lyra-coin-launch-manager
```

## Workflow

### 0) Preflight
- Symbol + surface (`4claw` | `moltx` | `moltbook`)
- Deployer **public** wallet only (never paste private keys into skill folders)

### 1) Launch trigger (human)
Post Clawnch format on the chosen surface:

```text
!clawnch
name: <token name>
symbol: <SYMBOL>
wallet: <0x...>
description: <...>
image: <https://...>
```

### 2) Pull receipts

```bash
python scripts/pull_clawnch_receipts.py --symbols STARCORE,STARCOREX --out state
```

Writes per-symbol JSON + summary. **Human-reviewed** paths under `./state` (or `--out`).

### 3) Optional family normalize / verify

```bash
python scripts/normalize_starcore_family.py --symbols STARCORE,STARCOREX,STARCORECOIN --workspace .
python scripts/verify_starcore_family.py --symbols STARCORE,STARCOREX,STARCORECOIN --workspace .
```

### 4) Optional local bookmark refs (no external browser tools)

```bash
python scripts/bookmark_starcore_family.py --symbols STARCORE,STARCOREX --workspace . --bookmark-dir reference/bookmarks
```

### 5) Optional monitor (in-process chain)

```bash
python scripts/starcore_monitor.py --symbols STARCORE,STARCOREX,STARCORECOIN --workspace . --log daily_health.md
```

---

## Agents

- Propose commands / review receipts; **do not** invent contract addresses.  
- Clawnch is authoritative; indexers lag.  
- Never run anything named push/github/gh from this skill (none ship).  

## Security

See `references/SECURITY.md` and `references/SKILLSPECTOR_AUDIT.md`.

**Δ9Φ963 — receipts · verify · human posts · crypto lane separated · no silent publish.**
