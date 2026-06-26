# hermes-for-win - Reference Documentation

## What is this?

`hermes-for-win` is a complete toolkit for installing, configuring, and managing hermes Agent and hermes-webui on Windows systems. It solves the problem of complex WSL setup for Windows users.

## Key Features

- **One-click Installation** - Download, configure, and start both services automatically
- **Windows Integration** - Uses Windows Task Scheduler for auto-start
- **Background Running** - No console windows, runs silently in background
- **Easy Management** - PowerShell scripts for start/stop/update/status
- **Self-updating** - Check and apply updates from GitHub automatically

## System Requirements

- Windows 10 (version 2004+) or Windows 11
- WSL2 enabled with Ubuntu installed
- At least 4GB RAM
- 5GB free disk space

## Quick Start

### 1. Install WSL2 (if not already installed)

Open PowerShell as Administrator:

```powershell
wsl --install
```

Restart your computer when prompted.

### 2. Run the installer

```powershell
cd .trae\skills\hermes-for-win\scripts
.\install-hermes.ps1
```

### 3. Access the WebUI

Open your browser and go to:
http://localhost:8788

## Script Reference

### install-hermes.ps1
The main installation script. Downloads, configures, and starts everything.

**What it does:**
1. Checks system requirements (WSL, Ubuntu)
2. Creates installation directory
3. Downloads latest hermes-agent and hermes-webui
4. Extracts and sets up files
5. Copies startup scripts to WSL
6. Configures Windows Task Scheduler
7. Starts services for first time

**Usage:**
```powershell
.\install-hermes.ps1
```

---

### check-status.ps1
Checks if services are running and shows status.

**Usage:**
```powershell
.\check-status.ps1
```

**What it shows:**
- WSL status
- Running processes
- Scheduled Task status
- Log file locations

---

### start-services.ps1
Starts hermes Agent and WebUI if they're not already running.

**Usage:**
```powershell
.\start-services.ps1
```

---

### stop-services.ps1
Stops all hermes-related processes.

**Usage:**
```powershell
.\stop-services.ps1
```

---

### update-hermes.ps1
Checks GitHub for latest versions and updates if needed.

**What it does:**
1. Fetches latest release info from GitHub
2. Compares with installed versions
3. Stops running services
4. Backs up current installation
5. Downloads and extracts updates
6. Restarts services

**Usage:**
```powershell
.\update-hermes.ps1
```

---

### setup-autostart.ps1
Configures (or re-configures) the Windows Scheduled Task for auto-start.

**Usage:**
```powershell
.\setup-autostart.ps1
```

---

## Directory Structure

```
%USERPROFILE%\.hermes-for-win\
├── hermes-agent-<version>\     # hermes Agent installation
├── hermes-webui-<version>\     # hermes WebUI installation
├── hermes_autostart.sh          # Startup script (copied to WSL)
└── backup-<timestamp>\          # Backup directories (created during updates)

WSL (Ubuntu):
/root/
├── hermes_autostart.sh          # Startup script
└── hermes_logs\                 # Log files
    ├── autostart.log
    ├── hermes_agent.log
    └── hermes_webui.log
```

## Troubleshooting

### Problem: Services won't start

**Check WSL:**
```powershell
wsl -l -v
```

**Check logs in WSL:**
```powershell
wsl -u root -e bash -c 'tail -50 /root/hermes_logs/hermes_agent.log'
wsl -u root -e bash -c 'tail -50 /root/hermes_logs/hermes_webui.log'
```

### Problem: Port 8788 is already in use

Find and stop the process using the port:
```powershell
netstat -ano | findstr :8788
taskkill /PID <process-id> /F
```

### Problem: Auto-start doesn't work

Check Task Scheduler:
1. Press Win+R, type `taskschd.msc`
2. Look for "HermesForWinAutoStart" task
3. Check History tab for errors

Re-run the setup script:
```powershell
.\setup-autostart.ps1
```

### Problem: Need to completely reinstall

1. Stop services: `.\stop-services.ps1`
2. Delete installation directory: `Remove-Item -Recurse $env:USERPROFILE\.hermes-for-win`
3. Remove scheduled task: `Unregister-ScheduledTask -TaskName HermesForWinAutoStart -Confirm:$false`
4. Re-run installer: `.\install-hermes.ps1`

## Security Notes

- The scheduled task runs as your user with highest privileges
- API keys are stored in WSL in `/root/.hermes/.env`
- Keep your Windows user account secure
- Don't share your installation with untrusted users

## Uninstall

To completely remove hermes-for-win:

```powershell
# Stop services
cd .trae\skills\hermes-for-win\scripts
.\stop-services.ps1

# Remove scheduled task
Unregister-ScheduledTask -TaskName HermesForWinAutoStart -Confirm:$false

# Delete installation directory
Remove-Item -Recurse -Force $env:USERPROFILE\.hermes-for-win

# Optional: Remove WSL installation (if not used for anything else)
# wsl --unregister Ubuntu
```

## License

MIT License - feel free to use and modify!

## Contributing

Found a bug or want to improve this? Submit an Issue or PR!
