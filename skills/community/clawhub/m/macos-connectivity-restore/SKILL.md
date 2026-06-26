---
name: macos-connectivity-restore
description: Restores Universal Control and AirDrop settings on a managed Mac by resetting the relevant managed preference files and setting AirDrop discoverability to Contacts Only. Use when the user asks to reopen Link to Mac or iPad, re-enable Universal Control, unlock AirDrop, restore AirDrop receiving, or make these fixes persist after reboot.
---

# MacOS Connectivity Restore

## Purpose

This skill restores the two settings we previously repaired on this Mac:

1. Universal Control / `Link to Mac or iPad`
2. AirDrop availability plus AirDrop receiving mode

It is designed for managed Macs where these settings are forced by files under `/Library/Managed Preferences`.

## What This Skill Changes

Root-level managed preferences:

- `com.apple.universalcontrol.plist`
  - `Disable = false`
- `com.apple.applicationaccess.plist`
  - `allowUniversalControl = true`
  - `allowAirDrop = true`
- `com.apple.NetworkBrowser.plist`
  - `DisableAirDrop = false`

User-level preferences:

- `com.apple.sharingd`
  - `DiscoverableMode = "Contacts Only"`
- `com.apple.NetworkBrowser`
  - `DisableAirDrop = false`

## Scripts

- `scripts/restore-root.sh`
  - Run as root. Fixes the managed preference files under `/Library/Managed Preferences`.
- `scripts/restore-user.sh`
  - Run as the logged-in user. Sets AirDrop receiving mode to `Contacts Only`.
- `scripts/install-startup.sh`
  - Installs a LaunchDaemon and LaunchAgent so these settings are restored automatically after reboot/login.

## Default Workflow

When the user asks to reapply these settings:

1. Run `scripts/restore-root.sh <username>` with admin privileges.
2. Run `scripts/restore-user.sh`.
3. Read back the values to verify:
   - `allowUniversalControl = 1`
   - `allowAirDrop = 1`
   - `DisableAirDrop = 0`
   - `DiscoverableMode = "Contacts Only"`

## Persist Across Reboots

When the user asks to make the change stick after every reboot:

1. Ensure this skill has been installed to a stable path under `~/.claude/skills/macos-connectivity-restore`.
2. Run `scripts/install-startup.sh`.
3. Confirm these startup items exist:
   - `/Library/LaunchDaemons/com.joseph.macos-connectivity-restore.root.plist`
   - `~/Library/LaunchAgents/com.joseph.macos-connectivity-restore.user.plist`

## Verification Commands

```bash
defaults read '/Library/Managed Preferences/com.apple.applicationaccess.plist' 2>/dev/null | rg 'allowAirDrop|allowUniversalControl'
defaults read '/Library/Managed Preferences/com.apple.NetworkBrowser.plist' 2>/dev/null
defaults read com.apple.sharingd 2>/dev/null | rg 'DiscoverableMode'
```
