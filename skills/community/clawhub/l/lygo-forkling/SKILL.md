---
name: lygo-forkling
description: "LYGO Forkling — test champion limb that self-builds a local fork on the lattice. Binds to existing chart node CHAMPION_LYRA (does not replace Lightfather). Autonomous local loop: birth → tick tasks → Continuum-style claims → generation++. Dry-run Star Chart propose only. Use when building a self-running test agent, champion fork, self-improve loop, or /lygo-forkling. No git push, no live chart ingest."
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "⑂"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-forkling"
    requires:
      anyBins: [python, python3]
  lygo: true
  forkling: true
  test_champion: true
  signature: "Delta9Phi963-FORKLING-v1.0.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/lygo-forkling"
  parent_node: "CHAMPION_LYRA"
  permissions:
    network: false
    subprocess: false
    filesystem:
      write: "state/ with --i-consent"
    publish: false
    live_star_chart: false
---

# LYGO Forkling v1.0.0 ⑂

**A test champion that builds itself.** Parent seat is already live: **CHAMPION_LYRA**. Forkling does not take that seat and does not claim to be Lightfather.

Local autonomy: birth a fork → run tasks → verify falsifiable claims → snapshot a generation → enqueue the next improvement.  
Live chart: **dry-run propose only**. Human steward still ingests.

**Signature:** `Delta9Phi963-FORKLING-v1.0.0`

---

## When to use

- “Self-building agent / test champion / fork on the lattice”
- Want a running loop with tasks and measurable improve
- Dry-run a new `NODE_FORKLING_TEST` connected to `CHAMPION_LYRA`

## When NOT to use

- Replacing Lightfather or a council champion
- Silent live Star Chart write / git push / ClawHub publish

---

## Install

```bash
npx clawhub@latest install deepseekoracle/lygo-forkling
cd path/to/lygo-forkling
python scripts/self_check.py
```

---

## Commands

```bash
python scripts/forkling.py birth --i-consent
python scripts/forkling.py tick --i-consent
python scripts/forkling.py loop --ticks 8 --i-consent
python scripts/forkling.py status
python scripts/forkling.py propose
```

| Command | Writes | Live chart |
|---------|--------|------------|
| `birth` | `state/fork/` | no |
| `tick` / `loop` | fork + `state/generations/gen_NNNN` | no |
| `status` | none | no |
| `propose` | none (prints PENDING JSON) | **never** |

Improve is claim-gated. If claims fail, generation does not advance (`blocked_self_police`).

---

## Lattice bind

| Field | Value |
|-------|--------|
| Test node | `NODE_FORKLING_TEST` |
| Parent (LIVE) | `CHAMPION_LYRA` |
| Also connects | `SEAL_000`, `PORTAL_STAR_CHART` |
| Council | The 15 champions already have galaxies/nodes. Forkling is a **child limb**, not a 16th seat. |

To go LIVE: gate the `propose` JSON → `haven_star_chart_submit.py --i-consent` → steward ingest. Forkling will not do that itself.

---

## Pair with

`lygo-cyborg-kernel` (task runner) · `lygo-continuum` (richer capsules) · `lygo-haven-star-chart` (gate) · `lygo-champion-lightfather` (persona, not identity theft)

**Δ9Φ963 — fork locally · prove claims · human remains publisher.**
