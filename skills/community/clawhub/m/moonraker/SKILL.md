---
name: moonraker
description: Control and monitor a Klipper 3D printer via the Moonraker API — print status, temps, pause, resume, cancel, emergency stop.
metadata: {"openclaw":{"requires":{"env":["MOONRAKER_HOST"],"bins":["curl"]},"primaryEnv":"MOONRAKER_HOST","emoji":"🖨️"}}
---

Control your 3D printer via the Moonraker REST API.

- **Host:** `http://$MOONRAKER_HOST:7125`
- **Helper script:** `{baseDir}/moonraker.sh`

---

## Quick Commands (via moonraker.sh)

```bash
moonraker.sh status   # print progress, temps, state
moonraker.sh pause    # pause current print
moonraker.sh resume   # resume paused print
moonraker.sh cancel   # cancel current print
moonraker.sh estop    # EMERGENCY STOP (firmware restart required after)
moonraker.sh files    # list gcode files on printer
```

---

## API Reference

Base URL: `http://$MOONRAKER_HOST:7125`

### Get Printer State
```
GET /printer/info
```
Returns firmware version, Klipper state (`ready`, `error`, `shutdown`, etc.), hostname.

### Get Print Stats + Temperatures
```
GET /printer/objects/query?print_stats&heater_bed&extruder
```
Returns:
- `print_stats.state` — `standby`, `printing`, `paused`, `complete`, `error`
- `print_stats.filename` — currently loaded file
- `print_stats.print_duration` — seconds elapsed
- `print_stats.total_duration` — total time since start
- `extruder.temperature` / `extruder.target` — hotend actual/target °C
- `heater_bed.temperature` / `heater_bed.target` — bed actual/target °C

### Pause Print
```
POST /printer/print/pause
```

### Resume Print
```
POST /printer/print/resume
```

### Cancel Print
```
POST /printer/print/cancel
```

### Emergency Stop
```
POST /printer/emergency_stop
```
⚠️ Immediately halts all motion and heaters. Klipper must be restarted via `POST /printer/firmware_restart` before printing again.

### List GCode Files
```
GET /server/files/list
```
Returns array of files in the `gcodes` directory with name, size, and modified time.

### Firmware Restart (after emergency stop)
```
POST /printer/firmware_restart
```

---

## Raw curl Examples

```bash
# Printer state
curl -s http://$MOONRAKER_HOST:7125/printer/info | jq .

# Temps + print stats
curl -s "http://$MOONRAKER_HOST:7125/printer/objects/query?print_stats&heater_bed&extruder" | jq .

# Pause
curl -s -X POST http://$MOONRAKER_HOST:7125/printer/print/pause | jq .

# Resume
curl -s -X POST http://$MOONRAKER_HOST:7125/printer/print/resume | jq .

# Cancel
curl -s -X POST http://$MOONRAKER_HOST:7125/printer/print/cancel | jq .

# Emergency stop
curl -s -X POST http://$MOONRAKER_HOST:7125/printer/emergency_stop | jq .

# List files
curl -s http://$MOONRAKER_HOST:7125/server/files/list | jq .
```

---

## Notes

- All POST endpoints return `{"result": "ok"}` on success.
- If Klipper is in error/shutdown state, most commands will fail until a firmware restart.
- Progress percentage = `print_stats.print_duration / print_stats.total_duration * 100` (approximate; more accurate progress available via `virtual_sdcard` object).
- For precise progress: `GET /printer/objects/query?virtual_sdcard` → `virtual_sdcard.progress` (0.0–1.0).
