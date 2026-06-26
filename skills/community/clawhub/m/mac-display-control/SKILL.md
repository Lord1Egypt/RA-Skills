---
name: mac-monitor-brightness-control
description: >
  Step-by-step guide for controlling external display or monitor settings on a Mac without
  third-party GUI apps. Covers Apple Silicon and Intel Macs, all major display brands
  (LG, Dell, BenQ, Samsung, ASUS, etc.), all connection types (USB-C, DisplayPort, HDMI, DVI),
  and a software fallback for displays that don't support DDC/CI. Controls include
  brightness, contrast, volume, input source switching, color temperature, power, and more.
  Use this skill whenever a user wants to control external display brightness, volume,
  contrast, color, input, or any other setting via the command line or keyboard shortcuts on macOS.
---

# External Display Control on macOS (No Third-Party GUI Apps)

## Overview

macOS doesn't natively expose controls for third-party displays, but most modern displays
support **DDC/CI** — a protocol that lets software send commands directly to display hardware:
brightness, contrast, volume, input source, color temperature, power, and more.

**This skill is split into a setup section (below) and per-control reference files.**
Once set up, jump to the reference file for the control you need.

### Reference Files (read after setup)
| File | Controls covered |
|---|---|
| `references/brightness.md` | Brightness — scripts, keyboard shortcuts, cron presets |
| `references/contrast.md` | Contrast — tips for color-mode lock |
| `references/volume.md` | Display speaker volume, mute toggle |
| `references/input-source.md` | Input switching, KVM setup, per-brand codes |
| `references/color-temperature.md` | Color presets, RGB gain, night/day mode scripts |
| `references/power-and-misc.md` | Power on/off, rotation, factory reset, capability probing |

---

## Step 0 — Identify Your Setup

### What Mac chip?
```bash
uname -m   # arm64 = Apple Silicon | x86_64 = Intel
```
Or: Apple menu → About This Mac.

### How is your display connected?
| Cable | Apple Silicon | Intel |
|---|---|---|
| **USB-C / Thunderbolt** | ✅ Full DDC support | ✅ Full DDC support |
| **DisplayPort** | ✅ Works | ✅ Works |
| **HDMI (built-in port)** | ⚠️ Blocked on M1/M2 Mac Mini, M1 MBP, Mac Studio | ✅ Works |
| **HDMI via Thunderbolt adapter** | ✅ Usually works | ✅ Works |
| **DisplayLink dock** | ❌ No DDC | ❌ No DDC |

> If you're on Apple Silicon with HDMI and can't switch cables → jump to **Software Fallback**.

---

## Step 1 — Install the Right Tool

### Apple Silicon → `m1ddc`
```bash
brew install m1ddc
m1ddc display list    # your display should appear here
```

### Intel → `ddcctl`
```bash
brew install ddcctl
ddcctl -d 1 -p 1      # probe display 1 — lists supported controls
```

> **Homebrew not installed?**
> ```bash
> /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
> ```

---

## Step 2 — Quick Smoke Test

Verify DDC is working before scripting anything:

```bash
# Apple Silicon
m1ddc set luminance 30   # screen should visibly dim
m1ddc set luminance 80   # screen should brighten

# Intel
ddcctl -d 1 -b 30
ddcctl -d 1 -b 80
```

No change? → See **Software Fallback** below.

Multiple displays? Target a specific one:
```bash
m1ddc display list              # find index
m1ddc display 2 set luminance 60
ddcctl -d 2 -b 60               # Intel equivalent
```

---

## Step 3 — Set Up Shell Scripts

All controls work as one-line shell commands. Create a `~/scripts/` folder
and save scripts there so Automator, cron, and keyboard shortcuts can call them.

```bash
mkdir -p ~/scripts
```

Always use **full binary paths** in scripts — Automator and cron don't load your shell PATH:
- Apple Silicon: `/opt/homebrew/bin/m1ddc`
- Intel: `/usr/local/bin/ddcctl`

**See each `references/*.md` file for ready-to-paste scripts per control.**

Make scripts executable after creating them:
```bash
chmod +x ~/scripts/*.sh
```

---

## Step 4 — Keyboard Shortcuts (Automator)

Works for any script. Do this once per action you want to bind to a key.

1. Open **Automator** → New Document → **Quick Action**
2. "Workflow receives" → **no input** in **any application**
3. Add **Run Shell Script** → paste the full script path (e.g. `/Users/yourname/scripts/brightness-up.sh`)
4. Save as e.g. **Brightness Up**
5. **System Settings → Keyboard → Keyboard Shortcuts → Services → General**
6. Find your Quick Action → assign a shortcut (e.g. `⌃⌥↑`)

> If the shortcut doesn't fire: System Settings → Privacy & Security → Automation → grant access.

---

## Step 5 — Time-Based Presets (Optional)

Use cron to switch display settings automatically at certain times:

```bash
crontab -e
```

```
# Day mode at 8am
0 8  * * *  /Users/yourname/scripts/day-mode.sh

# Night mode at 9pm
0 21 * * *  /Users/yourname/scripts/night-mode.sh
```

See `references/color-temperature.md` for ready-made day/night scripts.

---

## Software Fallback (No DDC Support)

If your display doesn't respond to DDC (TVs, budget displays, DisplayLink docks),
use macOS **Gamma table control** to dim the image in software:

```bash
# Set brightness to 60% (range: 0.0–1.0)
osascript -e 'tell application "System Events" to set brightness of (first screen of (get every screen)) to 0.6'
```

As a script (`~/scripts/brightness-soft.sh`):
```bash
#!/bin/bash
# Usage: brightness-soft.sh 0.6
osascript -e "tell application \"System Events\" to set brightness of (first screen of (get every screen)) to ${1:-0.7}"
```

> ⚠️ Software dimming changes appearance only — no power saving, slight colour shift at
> low values. Hardware DDC is always preferable when available.

---

## Troubleshooting

| Symptom | Fix |
|---|---|
| `m1ddc display list` returns nothing | Must use USB-C; HDMI blocked on M1/M2 Mac Mini |
| Display found but control has no effect | DDC/CI may be off in OSD; or Dynamic Contrast is on |
| Wrong display changes | Use `m1ddc display 2 …` or `ddcctl -d 2 …` |
| Command not found in Quick Action | Use full path: `/opt/homebrew/bin/m1ddc` |
| Shortcut doesn't fire | System Settings → Privacy & Security → Automation |
| No DDC at all | Use Software Fallback (osascript gamma) |

---

## References

- `m1ddc` (Apple Silicon): https://github.com/waydabber/m1ddc
- `ddcctl` (Intel): https://github.com/kfix/ddcctl
- DDC/CI HDMI block on Apple Silicon: https://github.com/MonitorControl/MonitorControl#readme