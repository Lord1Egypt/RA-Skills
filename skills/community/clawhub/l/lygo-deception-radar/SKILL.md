---
name: lygo-deception-radar
description: "LYGO Deception Radar — public proof layer for Ops Detector. Rebuilds an anonymized radar feed + HTML dashboard from the public labeled discourse suite only. Shows strong vs weak vs clear bands with operational threshold 0.65. Not for doxing or private mail. No subprocess. Install clawhub:@deepseekoracle/lygo-deception-radar."
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "📡"
    homepage: "https://github.com/DeepSeekOracle/lygo-protocol-stack/tree/main/docs/skills/lygo-deception-radar"
    requires:
      anyBins: [python, python3]
  lygo: true
  proof_layer: true
  signature: "Delta9Phi963-DECEPTION-RADAR-v1.0.0"
  publisher: deepseekoracle
  permissions:
    network: false
    shell: false
    subprocess: false
    filesystem:
      read: "public suite / local ops-detector scripts"
      write: "radar_feed.json + optional HTML"
    publish: false
---

# LYGO Deception Radar v1.0.0

**Proof layer** for the lattice: show Ops Detector working on **public** samples.

Live (after deploy): https://deepseekoracle.github.io/lygo-protocol-stack/deception-radar/

## Rebuild

```bash
# needs lygo-ops-detector installed nearby or LYGO_STACK_ROOT
python scripts/build_radar_feed.py --write-html
# deploy copy for Pages:
python scripts/build_radar_feed.py --write-html \
  --out-json D:/lygo-protocol-stack/docs/deception-radar/radar_feed.json \
  --out-html D:/lygo-protocol-stack/docs/deception-radar/index.html
```

## Ethics

- Public suite / public samples only  
- Not person verdicts  
- Operational bar ≥ 0.65 (or high evasion)  
- Weak band = calibration ranking only  

## Pair

`lygo-ops-detector` · `lygo-kickstart-wizard` · Haven Star Chart

**Δ9Φ963 — prove with public receipts.**
