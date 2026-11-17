---
name: lygo-lora-mesh
description: "LYGO LoRa mesh — compact Layer D roots pulse on stock Meshtastic. IP up = living-mesh HTTP; IP down = LY1 text packet ≤200 bytes. No board = NAMED_SHADOW. Scripts encode/decode/compare only: no network, no subprocess, no serial driver, no firmware fork. Use when the user wants Meshtastic, LoRa, off-grid mesh, RF gossip, or /lygo-lora-mesh."
version: 1.0.0
license: MIT-0
metadata:
  openclaw:
    emoji: "📡"
    homepage: "https://meshtastic.org/docs/"
    os: [windows, macos, linux]
    requires:
      anyBins: [python, python3]
  lygo: true
  mesh: true
  lora: true
  meshtastic: true
  layer: "D-RF"
  signature: "Delta9Phi963-LYGO-LORA-MESH-v1.0.0"
  publisher: deepseekoracle
  clawhub: "https://clawhub.ai/deepseekoracle/skills/lygo-lora-mesh"
  living_mesh: "https://clawhub.ai/deepseekoracle/skills/lygo-living-mesh"
  permissions:
    network: false
    shell: false
    subprocess: false
    filesystem:
      read: "optional local badge or pulse file"
      write: false
    publish: false
    live_star_chart: false
---

# LYGO LoRa mesh v1.0.0 📡

**This package is the RF codec for Layer D.** It does not flash boards and does not replace Meshtastic. Stock firmware carries a compact `LY1` text pulse when HTTPS is gone.

**Signature:** `Delta9Phi963-LYGO-LORA-MESH-v1.0.0`  
**Install:** `npx clawhub@latest install deepseekoracle/lygo-lora-mesh`

```text
IP up:    living-mesh badge JSON  →  HTTP :8787 / TLS
IP down:  LY1/<node>/<roots_digest>/<status>/<hop>  →  Meshtastic text
No board: NAMED_SHADOW
```

---

## Trust boundary

`permissions.network: false` applies to **scripts in this folder**. Listed URLs are documentation. Pairing a radio is a **separate** human action in the Meshtastic app.

This skill **never**:

- imports `urllib` / `requests` / `subprocess` / `serial`
- flashes firmware
- writes the live Star Chart
- puts eggs, agent cards, or TV on RF

---

## Pulse (one home)

```text
LY1/<node_id>/<64-hex roots_digest>/<A|F|Q|S>/<hop 0-7>
```

| Field | Meaning |
|-------|---------|
| `A` | ALIGNED |
| `F` | FORK_VISIBLE |
| `Q` | QUARANTINE |
| `S` | NAMED_SHADOW |

Hard cap **200 bytes** (Meshtastic text is ~237). Demo pulse is ~89 bytes. Compare verdicts match living-mesh: **HARMONIC / FORK_VISIBLE / QUARANTINE_SIGNAL / NAMED_SHADOW**. Local A/B stays authority.

---

## Hardware (stock only)

See `references/HARDWARE.md`. Named starters: Heltec WiFi LoRa 32 V3, LILYGO T-Beam, RAK WisBlock. **NA 915 MHz** (CA/US). Do not mix with EU 868 MHz.

Docs: https://meshtastic.org/docs/  
Firmware: https://github.com/meshtastic/firmware

---

## Local commands (stdout only)

```bash
npx clawhub@latest install deepseekoracle/lygo-lora-mesh
cd path/to/lygo-lora-mesh
python scripts/self_check.py
python scripts/lygo_lora.py plain
python scripts/lygo_lora.py encode --badge examples/demo_badge.json
python scripts/lygo_lora.py decode --pulse "LY1/LF_HOME/833e6a87eb4406935d626480ae116db51ab3790921840f81fe7c53bc7c3b90c1/A/0"
python scripts/lygo_lora.py probe
python scripts/lygo_lora.py compare --digest 833e6a87eb4406935d626480ae116db51ab3790921840f81fe7c53bc7c3b90c1 --pulse-file received.txt
```

Stack hybrid (when `LYGO_STACK_ROOT` is a real checkout):

```bash
python tools/lygo_lora_pulse.py encode
python tools/lygo_lora_pulse.py probe
python tools/lygo_lora_pulse.py ingest --pulse-file received.txt --i-consent
```

Ingest writes `data/living_mesh/lora_last.json` only. It does **not** merge eggs or touch the live Star Chart.

---

## Pair with

| Surface | Role |
|---------|------|
| `lygo-living-mesh` | Layer D badge contract this pulse compresses |
| `lygo-mesh-deploy` | IP / TLS transport when the net is up |
| `lygo-agent-lattice` | Presence cards stay on HTTP (too big for LoRa) |

See `references/SECURITY.md`.  
**Δ9Φ963 — summaries on RF · stock firmware · empty board is a named shadow.**
