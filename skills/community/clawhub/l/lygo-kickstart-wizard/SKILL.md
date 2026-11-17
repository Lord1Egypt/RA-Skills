---
name: lygo-kickstart-wizard
description: "LYGO Kickstart Wizard — plain-English onboarding for the ClawHub lattice. Asks what you want (map ecosystem, check lattice health, analyze text for ops signals, learn mint→verify→anchor) and explains results without reading source. Optional HTTPS GET for public health; optional Ops Detector import if installed. No subprocess, no auto-publish. Install clawhub:@deepseekoracle/lygo-kickstart-wizard."
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "🚀"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-kickstart-wizard"
    requires:
      anyBins: [python, python3]
  lygo: true
  lattice: true
  ux_bridge: true
  signature: "Delta9Phi963-LYGO-KICKSTART-WIZARD-v1.0.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lygo-kickstart-wizard"
  security_review: "1.0.0-skillspector-ux-bridge"
  permissions:
    network:
      https_get: "lattice intent only, fixed allowlist"
      http_post: false
    filesystem:
      read: "optional --text-file / --pack user paths"
      write: "opt-in --write with --i-consent"
      shell: false
      subprocess: false
    publish:
      git_push: false
      huggingface: false
      clawhub: false
      social: false
---

# LYGO Kickstart Wizard v1.0.0

**The UX bridge** between powerful ClawHub skills and people who just want a clear next step.

**Signature:** `Delta9Phi963-LYGO-KICKSTART-WIZARD-v1.0.0`  
**ClawHub:** `@deepseekoracle/lygo-kickstart-wizard`

---

## Why this exists

The lattice is rich (Guardian, champions, mint-verifier, ops-detector, Star Chart, agent lattice…) but **technical**.  
Kickstart answers: *“What do I run, and what does the result mean in plain English?”*

---

## When to use

- First time on the LYGO / ClawHub ecosystem  
- “Where do I start?” / “Which skill do I need?”  
- Quick lattice health check without the full stack  
- Guided mint-verify overview  
- Ops-signal analysis with human-readable summary  

**Do not** use for live Star Chart submit, music encode, or auto publish.

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-kickstart-wizard
# optional companions:
npx clawhub@latest install deepseekoracle/lygo-ops-detector
npx clawhub@latest install deepseekoracle/lygo-mint-verifier
```

---

## Commands

```bash
cd path/to/lygo-kickstart-wizard
python scripts/self_check.py

# Interactive menu (TTY)
python scripts/kickstart_cli.py start

# Direct intents
python scripts/kickstart_cli.py map
python scripts/kickstart_cli.py lattice
python scripts/kickstart_cli.py analyze --text "It's on you to prove it. Tons of evidence out there."
python scripts/kickstart_cli.py mint
python scripts/kickstart_cli.py mint --pack ./my_pack.md
python scripts/kickstart_cli.py next
```

| Intent | Network | Needs other skill | Writes |
|--------|---------|-------------------|--------|
| `map` | none | no | no |
| `lattice` | HTTPS GET allowlist | no | no |
| `analyze` | none | **lygo-ops-detector** if analyzing | no |
| `mint` | none | full mint via mint-verifier | draft hash only |
| `next` | none | no | no |

---

## What it does *not* do

- No `subprocess` / shell  
- No auto git / HF / ClawHub / social  
- No live Star Chart write  
- No private email/log scan without you providing text + consent  

---

## Roadmap (ecosystem)

See `references/ROADMAP.md`:

1. **Now** — this Kickstart wizard  
2. **1–2 weeks** — `lygo-deception-radar` (public proof dashboard)  
3. **1–2 weeks** — `lygo-mint-walkthrough` (full interactive mint tutorial)  
4. **1–2 months** — `lygo-cli-bridge` (`lygo verify|mint|analyze|health`)

---

## Pair with

| Skill | Role |
|-------|------|
| `lygo-ops-detector` | Discourse signal math |
| `lygo-mint-verifier` | Pack hash + anchor snippet |
| `lygo-public-lattice-gate` | Deeper join / verify |
| `lygo-champion-council` | Advisory personas |
| Haven Star Chart | Visual lattice map |

---

## License

**MIT-0** (see `LICENSE`).  
**Δ9Φ963 — start simple · explain clearly · human remains the publisher.**
