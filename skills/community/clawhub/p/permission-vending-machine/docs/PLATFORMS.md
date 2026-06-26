# Platform-Specific Setup

## macOS

### Requirements
- Python 3.9+
- SQLite (built into macOS Python)
- [`sendblue` CLI](https://pypi.org/project/sendblue/) — for iMessage support

### Install sendblue CLI

```bash
brew install sendblue   # or: pip install sendblue
```

### Install PVM

```bash
git clone https://github.com/tylerdotai/permission-vending-machine.git
cd permission-vending-machine
pip install -e .
```

### Configure

```bash
cp config.example.yaml config.yaml
# Edit config.yaml with your Sendblue, email, Discord credentials
```

### Run as launchd service (recommended — auto-starts on boot)

```bash
launchctl load ~/Library/LaunchAgents/ai.flume.pvm.plist

# Check status
launchctl list | grep pvm
curl http://localhost:7823/health
```

### Run manually

```bash
cd permission-vending-machine
PYTHONPATH=src python3 -m pvm serve --port 7823
```

### Sendblue on macOS

The `sendblue` CLI uses the local **Messages app** to send iMessages — no separate SMS plan needed. It works with your personal Apple ID or a dedicated iMessage phone number.

---

## Linux

### Requirements
- Python 3.9+
- SQLite (`sudo apt install sqlite3` or equivalent)

### Install PVM

```bash
git clone https://github.com/tylerdotai/permission-vending-machine.git
cd permission-vending-machine
pip install -e .
```

### Configure

```bash
cp config.example.yaml config.yaml
# Edit config.yaml
```

**Note on Sendblue:** The Sendblue CLI only works on macOS (it uses the Messages app). On Linux, enable **Discord webhook**, **Email (IMAP/SMTP)**, **Telegram**, or **Slack** as your notification + approval channels instead. All other features (vault, wrappers, HTTP approval server) work identically.

### Run as systemd service

Create `/etc/systemd/system/pvm.service`:

```ini
[Unit]
Description=PVM Approval Daemon
After=network.target

[Service]
Type=simple
User=YOUR_USERNAME
WorkingDirectory=/home/YOUR_USERNAME/permission-vending-machine
ExecStart=/usr/bin/python3 -m pvm serve --port 7823
Restart=always
RestartSec=10
StandardOutput=append:/home/YOUR_USERNAME/pvm.log
StandardError=append:/home/YOUR_USERNAME/pvm.err.log
Environment=PYTHONPATH=/home/YOUR_USERNAME/permission-vending-machine/src

[Install]
WantedBy=multi-user.target
```

Then:

```bash
sudo systemctl daemon-reload
sudo systemctl enable pvm
sudo systemctl start pvm
sudo systemctl status pvm
```

### Run manually

```bash
cd permission-vending-machine
PYTHONPATH=src python3 -m pvm serve --port 7823
```

### Linux notes

- **Email poller**: Works via IMAP — configure your email provider's IMAP settings
- **Discord**: Set `http_approval_base` to your server's public IP or domain
- **Telegram / Slack**: Both work via webhooks — cross-platform friendly

---

## Windows

### Requirements
- Python 3.9+ ([python.org installer](https://www.python.org/downloads/))
- SQLite — included with Python, or install via `pip install pysqlite3`

### Install PVM

```powershell
git clone https://github.com/tylerdotai/permission-vending-machine.git
cd permission-vending-machine
pip install -e .
```

### Configure

```powershell
copy config.example.yaml config.yaml
# Edit config.yaml with your credentials
```

**Note on Sendblue:** The Sendblue CLI only works on macOS. On Windows, use **Discord webhook**, **Email (IMAP/SMTP)**, **Telegram**, or **Slack** as your notification + approval channels.

### Run as Windows Service (recommended)

Use [NSSM](https://nssm.cc/) to wrap the Python process as a Windows service:

```powershell
# Download and install nssm
choco install nssm -y   # via Chocolatey, or download directly

# Create the service
nssm install PVM "C:\Python39\python.exe" "-m pvm serve --port 7823"
nssm set PVM AppDirectory "C:\path\to\permission-vending-machine"
nssm set PVM AppEnvironment PYTHONPATH "C:\path\to\permission-vending-machine\src"
nssm set PVM DisplayName "PVM Approval Daemon"
nssm set PVM Description "Permission Vending Machine — AI agent approval system"
nssm set PVM Start SERVICE_AUTO_START

# Start it
nssm start PVM
```

Or use Task Scheduler for a simpler approach (no service, but less reliable):

```powershell
# Create a scheduled task that runs at logon
$action = New-ScheduledTaskAction -Execute "C:\Python39\python.exe" `
    -Argument "-m pvm serve --port 7823" `
    -WorkingDirectory "C:\path\to\permission-vending-machine"
$trigger = New-ScheduledTaskTrigger -AtLogOn
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "PVM" -RunLevel Highest
```

### Run manually

```powershell
cd permission-vending-machine
$env:PYTHONPATH = "C:\path\to\permission-vending-machine\src"
python -m pvm serve --port 7823
```

### Windows notes

- **Firewall**: Allow port 7823 through the firewall for HTTP approval links to work
- **IMAP email**: Configure your email provider's IMAP settings (gmail, outlook, icloud, etc.)
- **Discord/Telegram/Slack**: All work via webhooks — cross-platform friendly

---

## Platform Feature Comparison

| Feature | macOS | Linux | Windows |
|---------|-------|-------|---------|
| Core vault + wrappers | ✅ | ✅ | ✅ |
| Email (IMAP/SMTP) | ✅ | ✅ | ✅ |
| Discord webhook | ✅ | ✅ | ✅ |
| Telegram bot | ✅ | ✅ | ✅ |
| Slack webhook | ✅ | ✅ | ✅ |
| Sendblue iMessage | ✅ | ❌ | ❌ |
| HTTP approval server | ✅ | ✅ | ✅ |
| launchd service | ✅ | — | — |
| systemd service | — | ✅ | — |
| Windows Service/NSSM | — | — | ✅ |

**Sendblue iMessage** works only on macOS because it uses the local Messages app. For Linux/Windows, use any other channel as your approval path — Discord webhook with clickable links is the smoothest UX.
