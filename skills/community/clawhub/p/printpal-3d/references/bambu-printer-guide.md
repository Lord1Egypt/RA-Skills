# Bambu Lab Printer Control Guide

This reference covers how to operate Bambu Lab 3D printers (H2D, X1C, P1S, A1) using the `bambu` CLI. Use this when the PrintPal workflow needs to send a model directly to a printer, monitor a print, or manage the printer hardware.

## Prerequisites

- Printer must have **Developer Mode** enabled (Settings → LAN Only → Enable Developer Mode)
- Required info: printer IP address, serial number, LAN access code (shown on the touchscreen)
- CLI tool: `@versatly/bambu` installed globally (`npm i -g @versatly/bambu`)

## Initial Setup

```bash
bambu setup <ip> <serial> <access_code>
bambu ping   # confirm the connection works
```

Configuration is stored at `~/.bambu/config.json`.

## Print Workflow (after generating a model with PrintPal)

Once a `.3mf` or sliced file is ready:

```bash
# Upload and start printing in one step
bambu job upload-and-print ./part.3mf

# Watch progress until complete
bambu watch
```

## Checking Printer State

```bash
bambu status            # full overview (state, temps, progress)
bambu status --json     # machine-readable (pipe to jq)
bambu temp              # temperatures only
bambu ams               # filament/AMS tray info
bambu errors            # active error codes
```

Quick readiness check:
```bash
bambu status --json | jq '.gcode_state'
# IDLE = ready, RUNNING = busy, FAILED = needs attention
```

## Controlling an Active Print

```bash
bambu pause     # pause current job
bambu resume    # continue after pause
bambu stop      # cancel the job entirely
```

## Temperature Presets

```bash
bambu heat nozzle:210 bed:60     # PLA
bambu heat nozzle:260 bed:100    # ABS
bambu heat nozzle:220 bed:70     # PETG
bambu cooldown                   # cool everything down
```

## Hardware Control

**Fans (0–100%):**
```bash
bambu fan part 80
bambu fan aux 50
bambu fan chamber 30
```

**Lights:**
```bash
bambu light on
bambu light off
```

**Movement:**
```bash
bambu home
bambu move x:10 y:20 z:5
bambu gcode "G28"    # raw gcode (use with caution)
```

## AMS Filament Management

```bash
bambu ams               # see what's loaded in each tray
bambu load 0            # select tray 0 as active
bambu load 2            # select tray 2
bambu unload            # unload current filament
```

## File Management

```bash
bambu files                       # list SD card contents
bambu upload ./part.3mf           # push file to printer
bambu delete old-print.3mf        # remove from SD card
```

## Calibration

```bash
bambu calibrate bed
bambu calibrate vibration
bambu calibrate flow
bambu calibrate all
```

## Shutdown Sequence

After a print finishes:
```bash
bambu cooldown
bambu light off
```

## Troubleshooting

- **Connection timeout** → Developer Mode enabled? Correct IP? Printer powered on?
- **Auth failed** → Re-check the LAN access code (it changes if Developer Mode is toggled off/on)
- **FTP error** → Port 990 with implicit TLS; printer must be in LAN-only mode
- **No AMS data** → Verify AMS is physically connected and detected on the touchscreen
- **MQTT drops** → Weak WiFi signal; check `bambu status` for `wifi_signal`

## Safety Notes

- Read-only commands (`status`, `temp`, `ams`, `errors`, `files`) are always safe to run.
- Commands like `print`, `stop`, `heat`, `move`, `gcode` physically control the printer. The nozzle reaches 200°C+ — exercise caution.
- `calibrate` moves the print head; ensure the bed is clear before running.
- `bambu gcode` sends raw commands — know exactly what you're sending.
