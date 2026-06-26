---
name: "3-Tier Auto-Backup — Daily Snapshots, Drive Mirror & Emergency Recovery"
description: "Automated backup in 3 layers: daily timestamped snapshots, secondary drive mirror, and emergency conversation export."
author: "@TheShadowRose"
version: "1.0.0"
tags: ["backup", "auto-backup", "disaster-recovery", "snapshots", "mirror", "workspace-protection", "windows"]
license: "MIT"
---

---

Never lose your AI workspace again. Three independent backup layers, each protecting against different failure modes.

## The 3 Tiers

| Tier | What | Protects Against | Frequency |
|------|------|-----------------|-----------|
| **1. Daily Snapshots** | Timestamped zip of workspace | Accidental deletions, bad edits | Daily (3 AM) |
| **2. Drive Mirror** | Full copy to secondary drive | Primary drive failure | Daily (after Tier 1) |
| **3. Emergency Export** | Standalone HTML chat backup | Total system failure | Always available |

## Setup

### Tier 1: Daily Snapshots

Edit `daily-backup.ps1` and set your paths:

```powershell
$WorkspacePath = "{YOUR_WORKSPACE_PATH}"
$BackupDir = "{YOUR_BACKUP_DIR}"
```

Register as a scheduled task:

```powershell
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-File {PATH_TO}\daily-backup.ps1"
$trigger = New-ScheduledTaskTrigger -Daily -At 3AM
Register-ScheduledTask -TaskName "AI Workspace Backup" -Action $action -Trigger $trigger
```

### Tier 2: Drive Mirror

If you have a secondary drive (D:, external USB, NAS), the backup script auto-syncs after creating the daily snapshot.

Edit the mirror path in `daily-backup.ps1`:
```powershell
$MirrorPath = "D:\WorkspaceBackup"
```

### Tier 3: Emergency Chat

`emergency-chat.html` is a standalone file that works in any browser with zero dependencies. It connects directly to your local Ollama instance.

Copy it to:
- Your Desktop
- Your secondary drive
- A USB stick

If everything else breaks, double-click this file.

## Restore Procedures

### From Daily Snapshot:
```powershell
Expand-Archive -Path "{BACKUP_DIR}\backup-YYYY-MM-DD.zip" -DestinationPath "{WORKSPACE}"
```

### From Drive Mirror:
```powershell
robocopy "D:\WorkspaceBackup" "{WORKSPACE}" /MIR
```

### From Emergency Chat:
Open the HTML file in a browser. Your conversation history won't be there, but you can communicate with your local AI immediately.

## Retention

Default: keeps last 7 daily snapshots. Older ones are auto-deleted. Change `$RetentionDays` in the script.
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

## Installation Note

The `daily-backup.ps1` PowerShell script is described in README.md. Create it manually in your workspace using the template provided. ClawHub does not distribute `.ps1` files directly.