---
name: meshtastic-detection
description: Receive DETECTION_SENSOR_APP alerts from Meshtastic LoRa devices via USB. When the remote sensor GPIO triggers (preset target detected), store the event and alert the user immediately.
metadata: {"openclaw": {"os": ["darwin", "linux"], "requires": {"anyBins": ["python3.12", "python3.11", "python3.10", "python3"]}, "emoji": "📡"}}
---

# Meshtastic Detection Skill

Receive detection sensor alerts from a remote Meshtastic device over LoRa. When the remote device's GPIO pin triggers (preset target detected), the event is stored locally and requires immediate user notification via feishu.

## Prerequisites

- Meshtastic-compatible hardware connected via USB (RAK4631, T-Beam, Heltec, etc.)
- Python 3.10+ with `meshtastic` and `pypubsub` packages (venv at `{baseDir}/venv`)
- `usb_receiver.py` daemon running
- Quick setup: `cd {baseDir} && ./setup.sh`
- Detailed guide: `{baseDir}/references/SETUP.md`

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     USB Receiver Daemon                       │
├──────────────────────────────────────────────────────────────┤
│  LISTEN:  DETECTION_SENSOR_APP only (GPIO trigger events)    │
│  STORE:   data/sensor_data.jsonl (append per detection)      │
│  LATEST:  data/latest.json (most recent detection)           │
└──────────────────────────────────────────────────────────────┘

┌─────────────┐     USB      ┌──────────────┐
│  LoRa Node  │◄────────────►│ usb_receiver │
│  (Radio)    │              │   daemon     │
└─────────────┘              └──────┬───────┘
                                    │
                    ┌───────────────┼───────────────┐
                    │               │               │
                    ▼               ▼               ▼
          sensor_cli.py     event_monitor.py   OpenClaw cron
          (query data)      (check alerts)     (feishu alert)
```

## Quick Reference

### Run the Receiver

```bash
cd {baseDir}
source venv/bin/activate
python scripts/usb_receiver.py --port /dev/cu.usbmodem1CDBD4A896441
```

### Check for New Alerts

```bash
cd {baseDir}
./venv/bin/python scripts/event_monitor.py
```

Every `DETECTION_SENSOR_APP` record = high-priority alert. Output:

```json
{
  "alerts": [{"priority": "high", "sender": "!1dd29c50", "text": "alert detected", "received_at": "...", "channel": "ch0", "portnum": "DETECTION_SENSOR_APP"}],
  "summary": "🚨 3 new detection alert(s) from 3 record(s)",
  "alert_count": 3,
  "new_records": 3
}
```

### Query Historical Data

```bash
python scripts/sensor_cli.py latest
python scripts/sensor_cli.py stats --since 24h
python scripts/sensor_cli.py query --since 1h
```

### Data Format

Each record in `data/sensor_data.jsonl`:

```json
{"received_at": "2026-03-04T11:07:06+00:00", "sender": "!1dd29c50", "channel": "ch0", "portnum": "DETECTION_SENSOR_APP", "data": {"type": "detection", "text": "alert detected"}}
```

**Only `DETECTION_SENSOR_APP` messages are captured.** This portnum means the remote sensor's GPIO pin was triggered — a preset target has been detected. **Every detection event requires immediate user alert.**

All other message types (TEXT_MESSAGE_APP, telemetry, position, etc.) are ignored.

### Log Rotation

`sensor_data.jsonl` is automatically rotated at **5 MB** (keeps 2 archive files, total max ~15 MB). Rotation is transparent — `event_monitor` auto-resets offset, `sensor_cli` reads across archives.

## Monitoring & Alerts

### Cron Job (Active)

The cron job runs `event_monitor.py` every 60 seconds and delivers alerts to feishu:

```bash
# Check status
openclaw cron list

# View run history
openclaw cron runs --id <job-id>

# Manual test
openclaw cron run <job-id>

# Edit config
openclaw cron edit <id> --timeout-seconds 60 --to <feishu-open-id>
```

Cron message template (for reference):

```
Run this command and report the output:
cd {baseDir} && ./venv/bin/python scripts/event_monitor.py
— If alert_count > 0, tell me how many alerts, the latest sender and time.
  If alert_count is 0, reply: 暂无新告警。
```

Key settings:
- `timeoutSeconds: 60` (agent needs ~20-40s)
- `channel: feishu`
- `delivery.to: ou_16c6dc8bda8ac97abfd0194568edee59`

### Alert Behavior

All `DETECTION_SENSOR_APP` events are treated as **high priority**. No rule configuration needed — every detection triggers an immediate alert. The alert message includes:
- Sender device ID
- Detection text (from remote sensor config)
- Timestamp

## Configuration

Edit `CONFIG.md` to customize:

- **Serial port** — USB device path
- **Notification channel** — `feishu` (configured in OpenClaw)

## Common Conversation Patterns

**User asks about recent detections:**
> "What was detected in the last hour?"

Run: `cd {baseDir} && ./venv/bin/python scripts/sensor_cli.py query --since 1h`

**User asks for statistics:**
> "Give me a summary of detections today"

Run: `cd {baseDir} && ./venv/bin/python scripts/sensor_cli.py stats --since 24h`

**User asks about system status:**
> "Is the sensor still working?"

Run: `cd {baseDir} && ./venv/bin/python scripts/sensor_cli.py status`

## Files

```
{baseDir}/
├── SKILL.md               # This file (agent instructions + metadata)
├── CONFIG.md              # User configuration
├── setup.sh               # One-click setup
├── scripts/
│   ├── usb_receiver.py    # USB serial daemon (DETECTION_SENSOR_APP only)
│   ├── event_monitor.py   # Incremental alert monitor
│   └── sensor_cli.py      # Query CLI
├── data/
│   ├── sensor_data.jsonl  # Detection records (auto-rotated at 5 MB)
│   ├── latest.json        # Most recent detection
│   └── monitor_state.json # Monitor byte offset + seen hashes
└── references/
    └── SETUP.md           # Detailed installation guide
```

## Troubleshooting

**"No records found"**
- Check that `usb_receiver.py` is running
- Verify USB device: `ls /dev/cu.usb*`

**"Resource temporarily unavailable"**
- Only one process can use the serial port. Check: `lsof /dev/cu.usbmodem*`

**Receiver connects but no data appears**
- The receiver only captures `DETECTION_SENSOR_APP` messages (other types are ignored)
- Run with `--debug` to see all packets: `python scripts/usb_receiver.py --port ... --debug`
- Verify the remote device is on the same channel and frequency
- Confirm the remote device has Detection Sensor Settings configured (GPIO pin monitoring)

**Cron job times out or fails delivery**
- Check: `openclaw cron runs --id <job-id>`
- Fix timeout: `openclaw cron edit <id> --timeout-seconds 60`
- Fix delivery: `openclaw cron edit <id> --to <feishu-open-id>`
