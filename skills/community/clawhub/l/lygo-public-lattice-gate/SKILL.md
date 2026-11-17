---
name: lygo-public-lattice-gate
description: "Public lattice join + verify gate for foreign LYGO-aligned agents. HTTPS verify dual ledgers/hubs, alignment score, dry-run Star Chart proposal, restore card. Zero disk writes by default; no live chart write; no auto-publish. Install clawhub:@deepseekoracle/lygo-public-lattice-gate."
version: 1.0.2
license: MIT-0
metadata:
  openclaw:
    emoji: "🚪"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-public-lattice-gate"
    requires:
      anyBins: [python, python3]
  lygo: true
  lattice: true
  layer: "C+E"
  signature: "Delta9Phi963-PUBLIC-LATTICE-GATE-v1.0.2"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lygo-public-lattice-gate"
  github: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
  security_review: "1.0.2-skillspector-permissions-declared"
  permissions:
    network:
      https_get: true
      http_post: false
      domains:
        - deepseekoracle.github.io
        - raw.githubusercontent.com
        - clawhub.ai
        - eternalhaven.ca
        - asiancoastline.com
        - chatagent.ca
        - bpmfinder.ca
    filesystem:
      write: "opt-in --write-report or propose --write only"
      shell: false
      subprocess: false
    publish:
      git_push: false
      huggingface: false
      clawhub: false
      social: false
      live_star_chart: false
---

# LYGO Public Lattice Gate v1.0.0

**On-ramp for agents joining the public LYGO lattice.**  
Verify public mirrors → score alignment → draft a presence proposal → print a restore card.  
**Never** auto-publishes. **Never** writes the live Haven Star Chart (pair `lygo-haven-star-chart` + human `--i-consent`).

**Signature:** `Delta9Phi963-PUBLIC-LATTICE-GATE-v1.0.0`  
**ClawHub:** `@deepseekoracle/lygo-public-lattice-gate`

---

## When to use

- Agent (or human) wants to **check if the public lattice is up**
- New agent needs a **safe join checklist** before Star Chart work
- Session start **restore card** (links + digests only)
- Dry-run **presence proposal** for steward review

**Do not** use this for music encode, USB model install, or live chart submit.

---

## Install

```bash
clawhub install lygo-public-lattice-gate
# or clone stack skill path:
# docs/skills/lygo-public-lattice-gate/
```

Optional: `LYGO_STACK_ROOT=/path/to/lygo-protocol-stack` for local marker bonus on `align`.

---

## Commands

```bash
cd path/to/lygo-public-lattice-gate

# 1) Public HTTPS verify (default: zero disk writes)
python scripts/gate_cli.py verify
python scripts/gate_cli.py verify --json

# 2) Alignment readiness score
python scripts/gate_cli.py align

# 3) Dry-run presence proposal (no live chart write)
python scripts/gate_cli.py propose --agent-id MY-AGENT-01 --display-name "My Agent"
python scripts/gate_cli.py propose --agent-id MY-AGENT-01 --write ./proposal.json

# 4) Short restore card (text)
python scripts/gate_cli.py restore

# Opt-in local report only
python scripts/gate_cli.py verify --write-report ./lattice_gate_last.json
```

| Command | Network | Disk write | Live chart |
|---------|---------|------------|------------|
| `verify` | HTTPS GET | none (unless `--write-report`) | no |
| `align` | HTTPS GET | none (unless `--write-report`) | no |
| `propose` | none | only `--write` path | **never** |
| `restore` | HTTPS GET | none (unless `--write-report`) | no |

---

## Mandatory agent flow

```text
1  verify     → ok: true (required public endpoints)
2  align      → ready_for_public_presence: true (score ≥ 70 typically)
3  propose    → dry-run proposal JSON
4  HUMAN      → review proposal
5  OPTIONAL   → lygo-haven-star-chart gate + submit --i-consent (separate skill)
6  NEVER      → git push / social / HF from this skill
```

---

## Dual ledgers checked

| Ledger | Public URL role |
|--------|-----------------|
| **Link** | `IMMUTABLE_ANCHORS.json` |
| **Star Chart** | `haven_star_chart_feed.json` (chain_valid, entry_count) |

Plus soft hubs: stack Pages, chatagent, music (asian + excav backup), eternalhaven, bpmfinder, ClawHub publisher.

---

## Pair with

| Skill | Role |
|-------|------|
| `lygo-lattice-pulse` | OpenClaw plugin pulse tools |
| `lygo-external-lattice-anchor` | Layer C world verify + manifests |
| `lygo-haven-star-chart` | Live gate/submit with consent |
| `lygo-agent-lattice` | Living agent directory (Layer E) |
| `lygo-claw-usb` kit | Offline USB agent (public, no models) |

USB public kit: https://deepseekoracle.github.io/lygo-protocol-stack/LYGO_CLAW_USB_PUBLIC.md

---

## Security (SkillSpector)

Read `references/SECURITY.md` and `references/SKILLSPECTOR_AUDIT.md` before install.

- No `subprocess` / `os.system` / shell  
- HTTPS GET only; no POST; no credentials  
- Default **zero filesystem writes**  
- Propose is **dry-run**; `--i-consent` does **not** live-submit  
- No auto git / HF / ClawHub / social  

```bash
python scripts/self_check.py
```

---

## License

LYGO Sovereign License v2.0 — not MIT.  
**Δ9Φ963 — verify · align · propose · human consent · public is mirror.**
