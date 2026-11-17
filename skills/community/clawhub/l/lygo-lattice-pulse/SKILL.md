---
name: lygo-lattice-pulse
description: "OpenClaw plugin skill — live Haven pulse, stack verify, registry compare, star chart gate, alignment readiness. Install clawhub:@deepseekoracle/lygo-lattice-pulse."
version: 1.1.0
license: LYGO-Sovereign-v2.0
metadata:
  openclaw:
    emoji: "💓"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
    requires:
      anyBins: [python, python3]
  lygo: true
  lattice: true
  openclaw_plugin: "lygo-lattice-pulse"
  signature: "Delta9Phi963-LYGO-LATTICE-PULSE-v1.1.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lygo-lattice-pulse"
  github: "https://github.com/DeepSeekOracle/lygo-protocol-stack"
---

# LYGO Lattice Pulse v1.1.0

**Plugin skill map** for live Haven lattice pulse tools.  
Install the OpenClaw plugin once; agents use the tool map below with human consent for any live chart write.

**Signature:** `Delta9Phi963-LYGO-LATTICE-PULSE-v1.1.0`  
**ClawHub:** `@deepseekoracle/lygo-lattice-pulse`

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-lattice-pulse
# OpenClaw plugin (when published as plugin package):
openclaw plugins install clawhub:@deepseekoracle/lygo-lattice-pulse
```

Set `LYGO_STACK_ROOT` to a trusted local clone of `lygo-protocol-stack` when running stack-bound tools.

---

## Tool map (plugin)

| Tool | When |
|------|------|
| `lygo_alignment_ready` | **Start here** — composite LIVE readiness score |
| `lygo_lattice_pulse` | Live registry SHA, cosmology, queue, feed |
| `lygo_registry_compare` | Local clone SHA vs GitHub Pages |
| `lygo_lattice_verify` | Stack marker files + alignment probe |
| `lygo_star_chart_gate` | Authoritative gate on submission JSON |
| `lygo_p0_quick_scan` | Fast text heuristic before posts |
| `lygo_consent_checklist` | Human `--i-consent` workflow |

---

## Mandatory flow before live writes

1. `lygo_alignment_ready` → `ready_for_live_ops: true`
2. `lygo_star_chart_gate` → `all_pass: true`
3. Human approves → submit only with explicit `--i-consent` (separate skill: `lygo-haven-star-chart`)

## Pair with

`lygo-protocol-stack-operator`, `lygo-haven-star-chart`, `lygo-lattice-birth`, `lygo-public-lattice-gate`

## Security

- No auto git push / ClawHub publish / social post from this skill  
- Live Star Chart writes require human consent via the dedicated chart skill  
- Read `references/SECURITY.md` and `references/SKILLSPECTOR_AUDIT.md`

```bash
python scripts/self_check.py
```

## License

LYGO Sovereign License v2.0 — not MIT.  
**Δ9Φ963 — pulse · verify · consent · then write.**
