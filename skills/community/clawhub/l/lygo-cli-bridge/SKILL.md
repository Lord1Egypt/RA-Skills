---
name: lygo-cli-bridge
description: "LYGO CLI Bridge — unified entrypoint: lygo health | map | analyze | mint | radar | next. Wraps kickstart + ops-detector + mint-walkthrough + deception-radar without exposing internal skill layout. In-process imports only; no subprocess; no auto-publish. Install clawhub:@deepseekoracle/lygo-cli-bridge."
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "⚡"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-cli-bridge"
    requires:
      anyBins: [python, python3]
  lygo: true
  cli: true
  signature: "Delta9Phi963-CLI-BRIDGE-v1.0.0"
  publisher: deepseekoracle
  permissions:
    network:
      https_get: "health intent only, fixed allowlist"
      http_post: false
    filesystem:
      read: "optional --text-file / --pack"
      write: "opt-in --out-json / mint ledger with --i-consent"
      shell: false
      subprocess: false
    publish:
      git_push: false
      huggingface: false
      clawhub: false
      social: false
---

# LYGO CLI Bridge v1.0.0

One entrypoint for common lattice power-user commands.

**Signature:** `Delta9Phi963-CLI-BRIDGE-v1.0.0`  
**ClawHub:** `@deepseekoracle/lygo-cli-bridge`

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-cli-bridge
# companions (recommended):
npx clawhub@latest install deepseekoracle/lygo-ops-detector
npx clawhub@latest install deepseekoracle/lygo-mint-walkthrough
npx clawhub@latest install deepseekoracle/lygo-deception-radar
```

## Commands

```bash
cd path/to/lygo-cli-bridge
python scripts/self_check.py

python scripts/lygo_cli.py version
python scripts/lygo_cli.py map
python scripts/lygo_cli.py health
python scripts/lygo_cli.py analyze --text "It's on you to prove it. Tons of evidence out there."
python scripts/lygo_cli.py mint
python scripts/lygo_cli.py mint --pack ./pack.md --i-consent
python scripts/lygo_cli.py radar
python scripts/lygo_cli.py radar --out-json ./radar_feed.json --write-html --i-consent
python scripts/lygo_cli.py next
```

| Command | Network | Needs companion | Writes |
|---------|---------|-----------------|--------|
| `version` / `map` / `next` | none | no | no |
| `health` | HTTPS GET allowlist | no | no |
| `analyze` | none | ops-detector | no |
| `mint` | none | mint-walkthrough (full) | with `--i-consent` |
| `radar` | none | deception-radar + ops-detector | with `--i-consent` |

## What it does *not* do

- No `subprocess` / shell  
- No auto git / HF / ClawHub / social  
- No live Star Chart write  
- Does not replace full engineer tools (protocol-stack-operator, mint-verifier production ledgers)

## Pair with

| Skill | Role |
|-------|------|
| `lygo-kickstart-wizard` | Plain-English onboarding menu |
| `lygo-ops-detector` | Discourse signal math |
| `lygo-mint-walkthrough` | Interactive mint tutorial |
| `lygo-deception-radar` | Public proof feed |
| Haven Star Chart | Visual lattice map |

## License

**MIT-0** (see `LICENSE`).  
**Δ9Φ963 — one CLI · local-first · human remains the publisher.**
