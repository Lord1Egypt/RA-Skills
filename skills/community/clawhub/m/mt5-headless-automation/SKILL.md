---
name: "mt5-headless-automation"
description: "Run MetaTrader 5 (MT5) fully headless on Linux/VPS: Wine + Xvfb + xdotool + OCR. Install, log in, attach EAs, deploy experts, monitor heartbeat and auto-restart. Built from real production experience (Vantage, 17 symbols, DRT-Axe EA). Perfect for traders who want to run EAs 24/7 without a screen. ⚠️ WARNING: runs system-level commands (wine, Xvfb, sudo apt), can restart MT5/terminate processes, and handles broker login credentials."
metadata: {"mt5-headless-automation": {"requires": {"bins": ["wine", "xvfb", "xdotool", "tesseract", "scrot", "sudo"], "files": ["~/.config/tg-alert.env"], "env": ["MT5_ACCOUNT", "MT5_PASSWORD"]}, "permissions": {"exec": ["bash", "wine", "xvfb-run", "xdotool", "import", "tesseract", "sudo"], "network": ["api.telegram.org"], "files": ["/tmp", "~/.config/tg-alert.env"], "notes": "GUI automation (xdotool) sends keystrokes to the MT5 window — verify the correct window has focus before running. Screenshots (import -window root) capture the ENTIRE display and may contain trading data, account details or other sensitive on-screen content — treat as sensitive artifacts: they are written to a private mktemp dir and auto-removed on exit. Keep keys scoped and never log them."}}}
---

# MT5 Headless Automation 🖥️🤖

Run MetaTrader 5 on a server WITHOUT a screen — full EA automation 24/7.

## ⚠️ Important (read first)

- **System-level actions:** this skill installs packages (sudo apt), starts Xvfb/Wine, and runs shell scripts. Review before running on production.
- **Restarts can interrupt trading:** the watchdog auto-restarts MT5 and may terminate EA processes during active sessions — this can detach strategies or affect open positions.
- **Credentials:** broker login (terminal64.exe via Wine) uses your MT5 account/password. They are entered into the terminal and may appear in process arguments or logs — store them in env vars or a protected file, never in scripts committed to git. Use a read-only/demo account for testing.
- **Built from production experience** — but backtest/production results are historical and not guaranteed.

## What this skill does

1. **Install MT5 + Wine + Xvfb** (headless display)
2. **Log in to broker account** (terminal64.exe via Wine)
3. **Attach EAs** via Navigator (Ctrl+N → OCR → double-click → Enter)
4. **Deploy EA changes** with 1 command (copy → compile → restart → verify)
5. **Monitor heartbeat** — auto-restart if the EA hangs
6. **Avoid the 5 classic pitfalls** (documented below)

## Quick start

```bash
# 1) Environment
sudo apt install wine xvfb xdotool tesseract-ocr scrot
Xvfb :99 -screen 0 1280x720x24 &
export DISPLAY=:99

# 2) Install MT5 (Windows installer via Wine)
wine "mt5setup.exe" /auto

# 3) Attach EA (scripts/attach_ea.sh)
bash scripts/attach_ea.sh "DRT-Axe"

# 4) Deploy new EA version (scripts/deploy_ea.sh)
bash scripts/deploy_ea.sh
```

## The 5 classic pitfalls (we have hit them ALL)

| # | Pitfall | Symptom | Fix |
|---|---------|---------|-----|
| 1 | **ArraySetAsSeries missing** | EA reads history backwards → 0 trades | `ArraySetAsSeries(rates, true)` after every CopyRates |
| 2 | **EA unloads on MT5 restart** | "EA running" but HB file frozen | Attach MANUALLY after each restart (auto-attach unreliable) |
| 3 | **Log freshness ≠ EA running** | False positive in monitor | Check HB file mtime, not log lines |
| 4 | **pkill -f kills itself** | Script dies suddenly | `pkill -f "pa[t]tern"` or `kill $(lsof -ti:PORT)` |
| 5 | **xdotool coordinates change** | Click on wrong place | OCR-find the element each time (tesseract + tsv) |

## Files

```
mt5-headless-automation/
├── SKILL.md
└── scripts/
    ├── attach_ea.sh     # OCR-guided EA attach via Navigator
    ├── deploy_ea.sh     # 1-command: copy → compile → restart → verify
    ├── watchdog.sh      # Heartbeat check + auto-restart
    └── ea_fix.py        # Diagnose why the EA is not trading
```

## Verification (always!)

- EA log: `MQL5/Files/<EA>_Log.txt` (server time GMT+3)
- Heartbeat: `<EA>_HB.txt` — mtime must be < 60 sec old
- Data: `<EA>_Data.json` (real-time klines every 60s)
- ex5 MD5 must match workspace copy after deploy
