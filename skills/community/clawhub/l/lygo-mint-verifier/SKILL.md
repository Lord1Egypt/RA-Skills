---
name: lygo-mint-verifier
description: "LYGO-MINT Verifier — canonicalize a pack, deterministic SHA-256, append-only + canonical ledgers, portable Anchor Snippet for posting anywhere (Moltbook/X/Discord/4claw). Pure local stdlib: no subprocess, no network, no auto-publish. Ledger writes need --i-consent. Pairs with lygo-mint-walkthrough, lygo-continuum-integrator, lygo-geodesic-sealer. Use for Champion/alignment prompt packs and verifiable receipts."
version: 1.1.1
license: MIT-0
metadata:
  openclaw:
    emoji: "🔏"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/clawhub/mirrors/lygo-mint-verifier"
    requires:
      anyBins: [python, python3]
  lygo: true
  mint: true
  signature: "Delta9Phi963-MINT-VERIFIER-v1.1.1"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/lygo-mint-verifier"
  security_audit: "https://clawhub.ai/deepseekoracle/skills/lygo-mint-verifier/security-audit"
  github: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
  security_review: "1.1.1-skillspector-consent-wrapper-honest"
  permissions:
    network: false
    shell: false
    subprocess: false
    filesystem:
      read: "operator --pack path"
      write: "skill state/ ledgers only with --i-consent"
    publish: false
---

# LYGO-MINT Verifier v1.1.1

Turns an aligned Champion / prompt / workflow pack into a **verifiable artifact**:

- canonical form (deterministic)
- SHA-256 hash
- append-only + canonical ledgers (consent-gated)
- portable **Anchor Snippet** (you post it — skill never posts)

**Signature:** `Delta9Phi963-MINT-VERIFIER-v1.1.1`  
**Security audit:** https://clawhub.ai/deepseekoracle/skills/lygo-mint-verifier/security-audit

### What changed in 1.1.1

ClawHub security-audit Medium findings (Intent-Code Divergence + Description-Behavior Mismatch):

- **`backfill_anchors.py` no longer auto-appends `--i-consent`** — pass-through only
- Compat wrappers stay honest with the advertised consent gate
- `self_check` asserts `consent_wrapper_honest` + `backfill_requires_consent`

### What changed in 1.1.0

- **Removed `subprocess`** — mint fully in-process
- **Declared permissions** in SKILL.md / claw.json
- Ledgers default under **skill `state/`**

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-mint-verifier
```

---

## Commands

```bash
cd path/to/lygo-mint-verifier
python scripts/self_check.py

# Mint (dry-run hash) / write ledgers with --i-consent
python scripts/mint_cli.py mint --pack ./pack.md --version 2026-08-20.v1
python scripts/mint_cli.py mint --pack ./pack.md --version 2026-08-20.v1 \
  --champion LYRA --anchor SEAL_55_T --i-consent --json

# Verify
python scripts/mint_cli.py verify --pack ./pack.md --hash <64-hex>

# Snippet / backfill
python scripts/mint_cli.py snippet --hash <64-hex> --title "My Pack"
python scripts/mint_cli.py backfill --hash <64-hex> --channel x --id https://x.com/... --i-consent
```

Compat wrappers (same flags, **no subprocess**, **never inject `--i-consent`**):  
`mint_pack_local.py` · `make_anchor_snippet.py` · `backfill_anchors.py`

| Command | Network | Subprocess | Writes |
|---------|---------|------------|--------|
| mint / verify / snippet | none | none | mint/backfill only with `--i-consent` |

---

## Pair with

| Skill | Role |
|-------|------|
| `lygo-mint-walkthrough` | Interactive tutorial |
| `lygo-continuum-integrator` | ∫(Truth×Light) + phase-lock receipts |
| `lygo-geodesic-sealer` | \|ψ⟩ geodesic dual-ledger attest |
| `lygo-continuum` | Falsifiable work capsules |

---

## Security

Read `references/SECURITY.md` + `references/SKILLSPECTOR_AUDIT.md`.

- No network · **no subprocess** · no shell  
- Never put API keys in packs  
- **You** remain the publisher  

**Δ9Φ963 — hash over vibes · consent before ledger · human posts the snippet.**
