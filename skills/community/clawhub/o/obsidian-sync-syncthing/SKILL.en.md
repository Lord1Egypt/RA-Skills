---
name: obsidian-sync-syncthing
description: Cross-platform Obsidian sync (Mac ↔ iPhone) powered by Syncthing — zero plugins, zero cost, offline-first, with intelligent large-file filtering.
author: KyleJia
license: MIT
version: 1.0.0
tags: [obsidian, syncthing, sync, ios, mac, offline-first, knowledge-management, self-hosted]
---

# Obsidian Cross-Platform Sync (Mac ↔ iPhone)

> **Zero Plugins · Zero Cost · Smart Filtering · Offline-First**

## Overview

This guide documents a complete setup for bidirectional Obsidian vault sync between Mac and iPhone using **Syncthing** — an open-source, peer-to-peer file synchronization tool. No iCloud, no Obsidian Sync subscription, and no Obsidian plugins required.

### Why This Solution?

| Feature | This Guide | Obsidian Sync | iCloud |
|---------|-----------|---------------|--------|
| Cost | **Free** | $4/month | Free (5GB) |
| Plugin Dependency | **None** | None | None |
| Smart Large-File Filtering | **✅ Yes** | ❌ | ❌ |
| Offline Access | **✅ Full** | ✅ | ⚠️ Requires pre-sync |
| Architecture | **✅ P2P Direct** | ❌ Cloud relay | ❌ Apple servers |
| End-to-End Encryption | **✅** | ✅ | ❌ |
| Cross-Platform | **✅ All platforms** | ✅ All platforms | Apple only |

### Architecture

```
┌─────────────┐         Syncthing (P2P)        ┌─────────────┐
│     Mac     │◄──────────────────────────────►│   iPhone    │
│             │     End-to-end encrypted        │             │
│  Syncthing  │     LAN direct connection       │ Möbius Sync │
│  (Server)   │     No third-party servers      │  (Client)   │
│             │                                 │             │
│  Obsidian   │                                 │  Obsidian   │
│  Vault/     │                                 │  Local Dir/ │
│  ...        │                                 │  ...        │
└─────────────┘                                 └─────────────┘
```

### Smart Large-File Filtering

The sync process automatically excludes large files to save device storage:

- Archives: `*.7z`, `*.zip`, `*.rar`
- Videos: `*.mp4`, `*.mov`, `*.avi`
- Large presentations: `*.pptx` / `*.ppt` files **>50MB**

---

## Prerequisites

| Device | Requirements |
|--------|-------------|
| Mac | macOS 11+, Syncthing installed via Homebrew |
| iPhone | iOS 15+, Möbius Sync installed (free on App Store) |
| Network | Both devices on the same LAN, or configured for remote discovery |

---

## Step 1: Mac Setup

### 1.1 Install Syncthing

```bash
# Install via Homebrew
brew install syncthing

# Start Syncthing (background)
brew services start syncthing

# Or run in foreground (for initial setup)
syncthing
```

### 1.2 Open the Web UI

Navigate to `http://127.0.0.1:8384` in your browser.

### 1.3 Record Your Device ID

In the Web UI → Actions → Show ID. Copy the device ID — you'll need it for the iPhone setup.

### 1.4 Enable Auto-Start

```bash
brew services start syncthing
```

### 1.5 Add a Sync Folder

1. Web UI → Folders → Add Folder
2. **Folder Label**: `Obsidian Vault`
3. **Folder Path**: Your vault path, e.g. `~/Documents/Obsidian Vault`
4. **File Versioning**: Enable "Simple File Versioning" (keep last 5 versions recommended)
5. Save

---

## Step 2: iPhone Setup

### 2.1 Install Möbius Sync

Search "**Möbius Sync**" on the App Store and install (free).

> Note: The free version limits sync to 20MB. For larger vaults, the one-time in-app purchase is ¥38 (~$5.30 USD).

### 2.2 Add Device (Pair with Mac)

1. Open Möbius Sync → Devices → +
2. Enter your Mac's device ID (from Step 1.3)
3. Set a device name (e.g., your Mac's hostname)
4. Save and wait for pairing

### 2.3 Confirm Pairing on Mac

Return to the Syncthing Web UI (`http://127.0.0.1:8384`). You'll see the iPhone's pairing request — click **Add Device**.

### 2.4 Add Sync Folder

**Critical step: Point the sync target to Obsidian's local directory.**

1. Möbius Sync → Folders → + → Add Folder
2. **Folder Label**: `Obsidian Vault`
3. **Folder Path**: Select Obsidian's local directory on iPhone
   - Path: Files app → On My iPhone → Obsidian → Obsidian Vault
4. **Shared With**: Check your Mac device
5. Save

### 2.5 Confirm Sharing on Mac

Return to the Syncthing Web UI and confirm the iPhone's folder sharing request.

### 2.6 Verify Sync Status

- Möbius Sync shows folder status as **Running**
- Open the Obsidian app on iPhone — all notes should be visible

---

## Step 3: Smart Large-File Filtering

### 3.1 Create the Exclusion Script

Create a sync script on Mac that automatically excludes large files:

```python
#!/usr/bin/env python3
"""Sync Obsidian Vault with smart large-file exclusion."""
import subprocess, os, tempfile

SRC = "~/Documents/Obsidian Vault"      # Replace with your vault path
DST = "~/iCloud/Obsidian Vault"         # Replace with your target path

# Find PPT files >50MB
result = subprocess.run(
    ["find", os.path.expanduser(SRC), "-type", "f",
     "(", "-name", "*.pptx", "-o", "-name", "*.ppt", ")", "-size", "+50M"],
    capture_output=True, text=True
)
big_ppts = result.stdout.strip().split("\n") if result.stdout.strip() else []

# Generate exclude-from file
exclude_tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
exclude_tmp.write("*.7z\n*.zip\n*.rar\n*.mp4\n*.mov\n*.avi\n")
for f in big_ppts:
    if f:
        rel = f.replace(os.path.expanduser(SRC) + "/", "")
        exclude_tmp.write(rel + "\n")
exclude_tmp.close()

# rsync
cmd = ["rsync", "-av", "--update", f"--exclude-from={exclude_tmp.name}",
       f"{os.path.expanduser(SRC)}/", f"{os.path.expanduser(DST)}/"]
subprocess.run(cmd)
os.unlink(exclude_tmp.name)

print(f"✅ Sync complete. Excluded {len(big_ppts)} large PPT files.")
```

### 3.2 Run the Script

```bash
python3 sync-obsidian.py
```

---

## Step 4: Optimization

### 4.1 Password-Protect the Web UI

```bash
# Generate a password hash
syncthing generate --password

# Edit config (~/.config/syncthing/config.xml)
# Add inside <gui> tag:
#   <authenticationUser>admin</authenticationUser>
#   <authenticationPassword>your_hash_here</authenticationPassword>

# Restart
brew services restart syncthing
```

### 4.2 LAN-Only Sync (Better Battery Life)

Web UI → Settings → Connections → Enable **Local Discovery**, disable **Global Discovery**. Devices will only sync when on the same network.

### 4.3 File Versioning

Web UI → Folder Settings → File Versioning → Enable **Simple File Versioning** (keep last 5-10 versions recommended).

---

## Troubleshooting

### Q: iPhone folder status shows "Stopped"

**A**: Check if the Syncthing engine is enabled. In Möbius Sync → Settings, confirm the Syncthing service status is **Running**.

### Q: Free version 20MB limit

**A**: If your Obsidian vault exceeds 20MB, Möbius Sync disables sync on the free tier. The one-time in-app purchase (¥38 / ~$5.30 USD) removes this limit.

### Q: Sync delays or no auto-sync

**A**:
1. Confirm both devices are on the same LAN
2. Check iPhone background app refresh for Möbius Sync (Settings → General → Background App Refresh)
3. Manual trigger: Möbius Sync → Folder → Rescan

### Q: Conflict files

**A**: Syncthing preserves conflict versions (appends `.sync-conflict` suffix to the filename). No data is overwritten. Enable file versioning for extra safety.

### Q: Obsidian on iPhone shows empty vault

**A**: Verify Möbius Sync's sync path points to Obsidian's local directory (Files → On My iPhone → Obsidian → Obsidian Vault), not another directory.

### Q: How to exclude specific large files?

**A**: Add rules to the sync script's exclusion list, e.g., `*.psd` (design files), `*.ai`, etc.

---

## Technical Rationale

### Why Not an Obsidian Plugin?

Existing solutions (e.g., obsidian-syncthing-integration on GitHub) require installing a Syncthing plugin inside Obsidian. This introduces:

1. **Plugin maintenance dependency** — the solution breaks if the plugin is abandoned
2. **Obsidian resource overhead** — the plugin runs inside the app process
3. **Compatibility risk** — Obsidian updates can break plugin functionality

This guide operates at the **filesystem level**, completely decoupled from Obsidian — more stable and reliable.

### Why Not iCloud?

1. iCloud sync has noticeable delays (especially for large files)
2. Free tier is only 5GB
3. No smart file filtering capability
4. Requires Apple servers; no offline access without pre-sync

---

## License

MIT License — Author: KyleJia

Copyright (c) 2026 KyleJia

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
