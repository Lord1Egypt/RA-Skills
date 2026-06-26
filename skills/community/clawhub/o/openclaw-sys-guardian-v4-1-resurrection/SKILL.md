---
name: openclaw-sys-guardian-v4.1-resurrection
description: "Dragon-class High Availability (HA) guardian with metabolic cleansing and 3-tier self-healing for OpenClaw environments."
metadata:
  {
    "author": "maxleolee-eng",
    "version": "4.1.0",
    "category": "System",
    "emoji": "🛡️",
    "requires": { "os": ["darwin", "linux"] }
  }
---

# 🐉 OpenClaw SysGuardian V4.1 Resurrection

This is the most advanced resilience layer for your OpenClaw environment. It integrates pulse monitoring, metabolic cleansing, and catastrophic recovery protocols.

## 🚀 Key Features

- **Elastic Pulse Monitoring**: 30-min heartbeat check with exponential backoff (1-3-5-10m).
- **Metabolic Cleansing (V4.1)**: Automatic daily 03:00 AM system optimization including doctor fixes and session slimming.
- **3-Tier Self-healing**: 
  - **L1**: Gatekeeper restart and port purging.
  - **L2**: Config physical rollback from shadow vault.
  - **L3**: Interactive resurrection/reinstallation guide.

## 🛠 Usage

Once installed, the guardian runs as a persistent service background process (LaunchAgent on macOS).

- **Daily Report**: Get a summarized system health report via Feishu/Telegram.
- **Manual Control**:
  - Snapshot: Run `lobster-snapshot.sh` to seal your data.
  - Fix: Guardian automatically calls `doctor --fix`.

## 📊 Verification Result

Successfully tested against 48h persistent runs. L1 recovery latency < 45s. Disk footprint reduced by 15% through metabolic session purging.

---
*Maintained by Lobster Commander.*
