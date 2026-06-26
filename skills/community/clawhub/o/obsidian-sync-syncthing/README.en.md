# 🔄 Obsidian Cross-Platform Sync (Mac ↔ iPhone)

> **Zero Plugins · Zero Cost · Smart Filtering · Offline-First**

[中文版](./README.md) | [Hermes Skill](./SKILL.md) | [English Skill](./SKILL.en.md)

## Overview

Bidirectional Obsidian vault sync between Mac and iPhone using **Syncthing** — an open-source, peer-to-peer file synchronization tool.

- ✅ **Zero Cost** — Free and open-source, no subscription required
- ✅ **Zero Plugins** — Filesystem-level sync, completely decoupled from Obsidian
- ✅ **Smart Filtering** — Auto-excludes >50MB PPTs, videos, and archives
- ✅ **Offline-First** — P2P direct connection, no cloud relay needed
- ✅ **End-to-End Encrypted** — Data stays on your devices only

## Architecture

```
┌─────────────┐         Syncthing (P2P)        ┌─────────────┐
│     Mac     │◄──────────────────────────────►│   iPhone    │
│  Syncthing  │     E2E encrypted · LAN direct  │ Möbius Sync │
│  Obsidian   │                                 │  Obsidian   │
│  Vault/     │                                 │  Local Dir/ │
└─────────────┘                                 └─────────────┘
```

## Quick Start

### Mac

```bash
brew install syncthing
brew services start syncthing
# Open http://127.0.0.1:8384 to add sync folder
```

### iPhone

1. Install **Möbius Sync** from the App Store
2. Add your Mac's device ID (find it in Syncthing Web UI → Actions → Show ID)
3. Add sync folder pointing to `Files → On My iPhone → Obsidian → Obsidian Vault`

> Free tier is limited to 20MB. For larger vaults, the one-time in-app purchase is ¥38 (~$5.30 USD).

For detailed instructions, see [SKILL.en.md](./SKILL.en.md).

## Comparison

| Feature | This Guide | Obsidian Sync | iCloud | GitHub Plugin |
|---------|-----------|---------------|--------|---------------|
| Cost | **Free** | $4/mo | Free (5GB) | Free |
| Plugin Dependency | **None** | None | None | Required |
| Smart Large-File Filter | **✅** | ❌ | ❌ | ❌ |
| Offline Access | **✅** | ✅ | ⚠️ | ✅ |
| P2P / Decentralized | **✅** | ❌ | ❌ | ❌ |
| Maintenance Risk | **Low** | Low | Low | High |

## Files

| File | Description |
|------|-------------|
| `SKILL.md` | Chinese full tutorial (Hermes Skill format) |
| `SKILL.en.md` | English full tutorial |
| `README.md` | This file (Chinese) |
| `README.en.md` | English version of this file |

## License

[MIT](./LICENSE) — KyleJia
