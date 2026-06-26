# 🌌 Gravitational Wave Event Analyzer

> Fetch real LIGO/Virgo/KAGRA data. Detect black hole mergers. Run from your terminal.

A skill for [OpenClaw](https://openclaw.ai) that brings NASA/LIGO public gravitational wave data to your fingertips — no PhD required.

## What It Does

| Step | What Happens |
|------|--------------|
| 1 | Queries the GWOSC Catalog API for event metadata |
| 2 | Downloads real detector strain data (H1/L1/V1/K1) |
| 3 | Whitens + bandpass filters the signal |
| 4 | Computes Q-transform (time-frequency chirp signature) |
| 5 | Classifies merger type: BBH / BNS / NSBH |
| 6 | Generates plots + JSON + text report |

## Quick Start

```bash
# Install dependencies
pip install gwpy gwosc numpy scipy matplotlib astropy

# Analyze the first ever GW detection
python gw_analyzer.py --event GW150914 --detector H1 --output ./output/

# Analyze the most massive merger ever detected
python gw_analyzer.py --event GW231123_135430 --detector L1 --output ./output/

# List top 10 events from GWTC-3
python gw_analyzer.py --list-events --catalog GWTC-3 --top 10
```

## Output Files

```
output/
├── GW150914_H1_analysis.png      # 3-panel figure: raw strain, filtered, Q-transform
├── GW150914_H1_summary.json      # Machine-readable event parameters + results
└── GW150914_H1_report.txt        # Human-readable analysis report
```

## Notable Events

| Event | Type | Why It's Special |
|-------|------|------------------|
| `GW150914` | BBH | First gravitational wave ever detected (Sep 14, 2015) |
| `GW170817` | BNS | First neutron star merger + gamma ray burst + optical counterpart |
| `GW200105` | NSBH | First confirmed neutron star–black hole merger |
| `GW231123_135430` | BBH | Most massive black hole merger ever observed |

## Data Source

All strain data comes from [GWOSC (Gravitational Wave Open Science Center)](https://gwosc.org/), publicly released under **CC BY 4.0** license. This includes data from:
- **LIGO Hanford (H1)** — Washington, USA
- **LIGO Livingston (L1)** — Louisiana, USA  
- **Virgo (V1)** — Cascina, Italy
- **KAGRA (K1)** — Kamioka, Japan

## Science Background

Gravitational waves are ripples in spacetime caused by violent cosmic events — merging black holes, colliding neutron stars. They were first predicted by Einstein in 1916 and first detected by LIGO in 2015. The signal is a "chirp": frequency sweeps upward as objects spiral inward, then merges.

The Q-transform visualization shows this chirp signature — the sweeping curve is the gravitational wave itself, encoded in spacetime and detected on Earth.

## Merger Types

- **BBH** (Binary Black Hole) — Both objects > 3 M☉. Most common, loudest signal.
- **BNS** (Binary Neutron Star) — Both objects ≤ 3 M☉. Multi-messenger astronomy.
- **NSBH** (Neutron Star–Black Hole) — Mixed pair. Rarest, scientifically rich.

## License

MIT — built on GWOSC public data (CC BY 4.0).
