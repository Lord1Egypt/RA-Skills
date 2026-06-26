# OpenClaw Windows Fix — Idle Kill Bug

## The Problem

When OpenClaw runs as a Windows Scheduled Task, the default settings include an idle condition that kills the process after a period of inactivity. This means your agent goes offline randomly.

## The Fix

This script creates a corrected scheduled task that:
- Runs at user logon
- Does NOT stop on idle
- Restarts on failure (1 minute delay)
- Runs whether on battery or AC power

## Usage

### Option 1: Run the fix script (recommended)

Right-click `FIX_TASK.bat` → **Run as Administrator**

### Option 2: Manual fix

1. Open **Task Scheduler** (search for it in Start)
2. Find your OpenClaw task
3. Right-click → **Properties**
4. Go to **Conditions** tab
5. **UNCHECK** "Start the task only if the computer is idle"
6. **UNCHECK** "Stop if the computer ceases to be idle"
7. Go to **Settings** tab
8. **UNCHECK** "Stop the task if it runs longer than"
9. Set "If the task fails, restart every" to **1 minute**
10. Click OK

## FIX_TASK.bat Contents

```batch
@echo off
echo Fixing OpenClaw Scheduled Task...
echo.

REM Delete the old task
schtasks /delete /tn "OpenClaw Gateway" /f 2>nul

REM Create corrected task (runs at logon, no idle kill)
schtasks /create /tn "OpenClaw Gateway" /tr "cmd /c cd /d \"%USERPROFILE%\.openclaw\" && gateway.cmd" /sc ONLOGON /rl HIGHEST /f

echo.
echo Done! The task will now survive idle periods.
echo Restart your computer or run the task manually to apply.
pause
```

## How to Verify

After running the fix:
1. Open Task Scheduler
2. Find "OpenClaw Gateway"
3. Check Conditions tab — no idle conditions should be checked
4. Leave your computer idle for 30+ minutes
5. Check if OpenClaw is still running
---

## ⚠️ Disclaimer

This software is provided "AS IS", without warranty of any kind, express or implied.

**USE AT YOUR OWN RISK.**

- The author(s) are NOT liable for any damages, losses, or consequences arising from 
  the use or misuse of this software — including but not limited to financial loss, 
  data loss, security breaches, business interruption, or any indirect/consequential damages.
- This software does NOT constitute financial, legal, trading, or professional advice.
- Users are solely responsible for evaluating whether this software is suitable for 
  their use case, environment, and risk tolerance.
- No guarantee is made regarding accuracy, reliability, completeness, or fitness 
  for any particular purpose.
- The author(s) are not responsible for how third parties use, modify, or distribute 
  this software after purchase.

By downloading, installing, or using this software, you acknowledge that you have read 
this disclaimer and agree to use the software entirely at your own risk.


**DATA DISCLAIMER:** This software processes and stores data locally on your system. 
The author(s) are not responsible for data loss, corruption, or unauthorized access 
resulting from software bugs, system failures, or user error. Always maintain 
independent backups of important data. This software does not transmit data externally 
unless explicitly configured by the user.

---

## Support & Links

| | |
|---|---|
| 🐛 **Bug Reports** | TheShadowyRose@proton.me |
| ☕ **Ko-fi** | [ko-fi.com/theshadowrose](https://ko-fi.com/theshadowrose) |
| 🛒 **Gumroad** | [shadowyrose.gumroad.com](https://shadowyrose.gumroad.com) |
| 🐦 **Twitter** | [@TheShadowyRose](https://twitter.com/TheShadowyRose) |
| 🐙 **GitHub** | [github.com/TheShadowRose](https://github.com/TheShadowRose) |
| 🧠 **PromptBase** | [promptbase.com/profile/shadowrose](https://promptbase.com/profile/shadowrose) |

*Built with [OpenClaw](https://github.com/openclaw/openclaw) — thank you for making this possible.*

---

🛠️ **Need something custom?** Custom OpenClaw agents & skills starting at $500. If you can describe it, I can build it. → [Hire me on Fiverr](https://www.fiverr.com/s/jjmlZ0v)
