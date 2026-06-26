# systemd Service (Linux)

Run Kiwi Voice as a system service that starts on boot and auto-restarts on failure.

## Create the Service

Create `/etc/systemd/system/kiwi-voice.service`:

```ini
[Unit]
Description=Kiwi Voice Assistant
After=network.target sound.target

[Service]
Type=simple
User=kiwi
WorkingDirectory=/opt/kiwi-voice
ExecStart=/opt/kiwi-voice/venv/bin/python -m kiwi
Restart=on-failure
RestartSec=5
Environment=KIWI_LANGUAGE=en

[Install]
WantedBy=multi-user.target
```

## Enable and Start

```bash
sudo systemctl daemon-reload
sudo systemctl enable kiwi-voice
sudo systemctl start kiwi-voice
```

## View Logs

```bash
sudo journalctl -u kiwi-voice -f
```

## Commands

| Command | Action |
|---------|--------|
| `systemctl start kiwi-voice` | Start the service |
| `systemctl stop kiwi-voice` | Stop the service |
| `systemctl restart kiwi-voice` | Restart |
| `systemctl status kiwi-voice` | Check status |
| `systemctl enable kiwi-voice` | Enable on boot |
| `systemctl disable kiwi-voice` | Disable on boot |

## Audio Access

The service user needs access to audio devices. Add the user to the `audio` group:

```bash
sudo usermod -aG audio kiwi
```
