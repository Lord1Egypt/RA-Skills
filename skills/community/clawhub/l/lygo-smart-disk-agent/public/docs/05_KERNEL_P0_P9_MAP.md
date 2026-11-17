# Kernel P0–P9 map → Smart Disk

**Signature:** `Δ9Φ963-SDA-KERNEL-MAP-v1`  
**Normative UI refs:** Ethical-Chip-Firmware · Ethical-Chip-FirmwareV2 · LYGOGUARDIAN  

---

| Layer | Full stack meaning | SDA v1 implementation |
|-------|--------------------|------------------------|
| **P0** | Φ-gate / entropy / ethics pre-action | `kernel/p0_gate.py` + `firmware/seal.json` |
| **P1** | Mycelium memory | `kernel/p1_memory.py` → `data/mycelium/` |
| **P2** | Orchestration | Minimal: single agent loop in supervisor |
| **P3** | Consensus 3-6-9 | `kernel/p3_consensus.py` optional multi-sample |
| **P4** | Routing | Limb router in `agent/limbs.py` |
| **P5** | Action identity | `kernel/p5_identity.py` light-code per action |
| **P6** | Mesh | Status stub `lattice` limb |
| **P7** | Attestation | Seal hash in health |
| **P8** | HAIP / heartbeat | Daemon health loop |
| **P9** | TLS public mesh | Off by default (loopback HTTP) |

---

## Firmware seal fields

```json
{
  "signature": "Δ9Φ963-SDA-FIRMWARE-SEAL-v1",
  "ethical_chip_ref": "Ethical-Chip-FirmwareV2",
  "guardian_ref": "LYGOGUARDIAN",
  "policy": {
    "local_open_ui": true,
    "bind_loopback_only": true,
    "auto_publish": false,
    "p0_required": true
  }
}
```

**Δ9Φ963 — every layer either implemented or honestly stubbed.**
