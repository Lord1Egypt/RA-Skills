---
name: overrec-screen
metadata: {"version": "0.2.0"}
description: Use OverRec CLI to take screenshots, draw overlay rectangles, list monitors, find windows by title, or snap any app window to an exact position and size. Trigger when the user asks to screenshot a region, highlight/overlay an area, move/resize a window, fit a window to a rectangle, find a window by name, or capture what's on screen.
allowed-tools: Bash
---

You have access to OverRec CLI to control screen overlays, screenshots, and window placement.

## Environment

This skill runs on **Windows or WSL**. [OverRec](https://apps.microsoft.com/detail/9pdn41kpj3hg) must be installed and on the PATH.

- **Windows powershell**: use `OverRec.exe`
- **WSL**: use `pwsh.exe -C OverRec.exe` or `powershell.exe -C OverRec.exe`

**Check OverRec is available before running any command:**
```bash
OverRec.exe cli monitors 2>/dev/null || echo "OverRec not found"
```
If not found, inform the user that OverRec must be installed and on the PATH (or provide the full path if known).

---

## Available Commands

**List monitors:**
```
OverRec.exe cli monitors
OverRec.exe cli monitors --all
```

**Draw an overlay rectangle** (stays on top until timeout or closed):
```
OverRec.exe cli draw --location X,Y --size WxH [--color COLOR] [--monitor N] [--timeout SECONDS]
```
Colors: `red`, `green`, `blue`, `yellow`, `white`, `black`, or `#RRGGBB` hex. Default is blue.

**Take a screenshot:**
```
OverRec.exe cli screenshot --location X,Y --size WxH [--output FILE.png] [--no-clipboard] [--monitor N]
```
By default the image is copied to the clipboard. Use `--output` to also save to file. Use `--no-clipboard` to skip clipboard.

**Find a window by title keyword:**
```
OverRec.exe cli window [--all] [<keyword...>]
```
Lists visible windows whose title contains all given keywords (case-insensitive). Omit keywords to list every visible window.

- Default: compact ID/title table
- `--all`: also shows monitor number, location, and size (`max`/`min` for maximised/minimised)

Output format (default):
```
WindowID        Title
------------------------------------------------------------
657846          Google Chrome
329812          Visual Studio Code
```

Output format (`--all`):
```
WindowID        Mon   Location          Size          Title
--------------------------------------------------------------------------------
657846          0     0,0               1920x1080     Google Chrome
329812          0     max               1920x1080     Visual Studio Code
131070          1     1920,0            1280x720      Notepad
```

**Snap a window to an exact position and size:**
```
OverRec.exe cli snap --windowid ID --location X,Y --size WxH [--monitor N]
```
- `--windowid` — from `overrec cli window`
- `--location` / `--size` — in absolute screen coordinates, or relative to a monitor origin when `--monitor` is given
- DWM shadow margins are corrected automatically; the visible frame lands exactly at the requested rect
- The window is restored (if minimised/maximised) and brought to the front

---

## How to Handle User Requests

### "Take a screenshot of [area/region]"
1. If monitor layout is unknown, run `OverRec.exe cli monitors` first.
2. Determine or ask for X, Y, width, height.
3. Run screenshot command. Use `--output FILE.png` to save to disk; add `--no-clipboard` to skip clipboard copy.
4. Report the saved file path (or confirm it was copied to clipboard).

### "Highlight / draw an overlay on [area]"
1. Determine coordinates and size.
2. Run draw command. Use `--timeout` if the user wants it temporary.
3. Inform the user the overlay is active and how to dismiss it.

### "Search for a window / find window ID by name"
```bash
OverRec.exe cli window <keyword>
OverRec.exe cli window --all <keyword>   # also shows monitor, location, size
OverRec.exe cli window                  # list all visible windows
```
- Parse the output: skip the header (first 2 lines), then each line has `WindowID` (first field) and `Title` (rest).
- If no match, report that no window was found with that keyword.
- If multiple matches, show the list and ask the user which one to use.

Example — extract the first matching WindowID in bash:
```bash
WIN_ID=$(OverRec.exe cli window chrome | awk 'NR>2 && $1~/^[0-9]+$/ {print $1; exit}')
```

### "Snap / fit / move [app] into a rectangle"
Full workflow — search for the window then snap it:
```bash
# 1. Find the window
OverRec.exe cli window <keyword>

# 2. Snap it (use the WindowID from step 1)
OverRec.exe cli snap --windowid ID --location X,Y --size WxH

# 3. Optionally draw a brief overlay to confirm placement
OverRec.exe cli draw --location X,Y --size WxH --timeout 2
```

Combined one-liner (bash):
```bash
WIN_ID=$(OverRec.exe cli window chrome | awk 'NR>2 && $1~/^[0-9]+$/ {print $1; exit}')
OverRec.exe cli snap --windowid "$WIN_ID" --location 0,0 --size 1280x720
```

If `$WIN_ID` is empty, the window was not found — report this to the user.

### "Arrange windows side by side / tile windows"
1. List monitors: `OverRec.exe cli monitors --all`
2. Find each window by keyword.
3. Calculate tile rectangles from monitor dimensions.
4. Snap each window.

Example — split two windows left/right on a 1920×1080 primary monitor:
```bash
LEFT_ID=$(OverRec.exe cli window chrome  | awk 'NR>2 && $1~/^[0-9]+$/ {print $1; exit}')
RIGHT_ID=$(OverRec.exe cli window notepad | awk 'NR>2 && $1~/^[0-9]+$/ {print $1; exit}')
OverRec.exe cli snap --windowid "$LEFT_ID"  --location 0,0   --size 960x1080
OverRec.exe cli snap --windowid "$RIGHT_ID" --location 960,0 --size 960x1080
```

### "Watch / monitor [area] of the screen"
Implement a watch loop: repeatedly capture the region at an interval and save each frame.

```bash
INTERVAL=5
LOCATION="0,0"
SIZE="640x480"
OUTPUT_DIR="watch_output"
mkdir -p "$OUTPUT_DIR"
i=0
while true; do
    TIMESTAMP=$(date +%Y%m%d_%H%M%S)
    OverRec.exe cli screenshot --location "$LOCATION" --size "$SIZE" \
        --output "$OUTPUT_DIR/frame_${TIMESTAMP}.png" --no-clipboard
    echo "Captured frame $i at $TIMESTAMP"
    i=$((i+1))
    sleep "$INTERVAL"
done
```

Ask the user:
- What area to watch (coordinates + size, or ask them to describe the region)
- How often to capture (default: every 5 seconds)
- Where to save frames (default: `./watch_output/`)
- Stop condition: number of frames, duration, or manual stop

---

## Coordinate Tips
- Top-left of primary monitor is 0,0.
- For secondary monitors, use `OverRec.exe cli monitors --all` to find each monitor's `Abs Position`, then pass `--monitor N` so `--location` coordinates are relative to that monitor's origin.
- If the user describes a region vaguely ("top-right quarter of screen"), query monitors first to calculate coordinates.

## $ARGUMENTS

$ARGUMENTS
