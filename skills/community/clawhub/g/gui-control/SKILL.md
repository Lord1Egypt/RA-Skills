---
name: gui-control
description: Control the GUI desktop on this machine using xdotool, scrot, and Firefox. Use when the user asks to open a browser, visit a website, take a screenshot, click/type on screen, or interact with any GUI application. This machine has a display — it is NOT headless.
---

# GUI Control

Control the Linux desktop with a GUI display using shell tools.

## Environment

- **Display**: `DISPLAY=:1` — ALWAYS prefix all GUI commands with this
- **This machine has a display** — never say "I'm on a headless server"
- Tools available: `xdotool` (keyboard/mouse), `scrot` (screenshots), `firefox`

## Quick Reference

### Open Firefox with a URL

```bash
DISPLAY=:1 nohup firefox https://example.com > /dev/null 2>&1 &
```

Wait for page load before interacting:

```bash
sleep 5
```

### Take a Screenshot

```bash
DISPLAY=:1 scrot /tmp/screenshot.png
```

### Type Text into Active Window

```bash
DISPLAY=:1 xdotool type --delay 50 "Hello world"
```

### Press a Key

```bash
DISPLAY=:1 xdotool key Return
```

### Get Active Window Name

```bash
DISPLAY=:1 xdotool getactivewindow getwindowname
```

### Close Firefox

```bash
DISPLAY=:1 pkill firefox
```

## Workflow: Browse a Website and Interact

1. Open Firefox with URL: `DISPLAY=:1 nohup firefox <url> > /dev/null 2>&1 &`
2. Wait for load: `sleep 5`
3. Take screenshot to verify: `DISPLAY=:1 scrot /tmp/step.png`
4. Read screenshot to assess page state
5. Interact using keyboard (preferred over mouse):
   - `xdotool key Tab` — move focus
   - `xdotool key Return` — submit/confirm
   - `xdotool type --delay 50 "text"` — type into focused field
6. After each action, screenshot to verify result
7. Send screenshots to user with the `message` tool and `media` parameter

## Tips

- **Prefer keyboard over mouse coordinates** — Tab, Enter, arrow keys are more reliable than `xdotool mousemove` + `click`
- **YouTube shortcut**: press `/` to focus the search bar
- **Always wait** after page loads or actions before taking screenshots
- **Use `nohup ... &`** for launching Firefox so it doesn't block the shell
- **Send screenshots to user** using `message(content="...", media=["/tmp/screenshot.png"])`

## Lessons Learned

### Don't Over-Engineer
- **Start simple** — `xdotool` + keyboard shortcuts work great. Don't jump to Selenium/Marionette unless absolutely needed.
- **One clean attempt > five messy ones** — think before executing, don't retry the same failing approach.
- **Don't open Firefox multiple times** — check if it's already running first with `ps aux | grep firefox`

### Keyboard Shortcuts by Website
- **YouTube**: `/` focuses search bar, `Tab` navigates between elements, `Return` selects
- **General web**: `Ctrl+F` opens find bar, `Ctrl+L` focuses address bar, `Tab` cycles focus
- **Don't use `xdotool mousemove` with hardcoded coordinates** — they break on different resolutions and you might click the wrong element (e.g., address bar instead of YouTube search)

### Common Mistakes to Avoid
- ❌ **Don't guess coordinates** — `xdotool mousemove 640 120` will click different things on different screens
- ❌ **Don't say "I'm on a headless server"** — this machine HAS a display (`DISPLAY=:1`)
- ❌ **Don't use `DISPLAY=:0`** — the correct display is `:1`
- ❌ **Don't open multiple Firefox instances** — reuse the existing one or close it first
- ❌ **Don't confuse the browser address bar with website search bars** — use keyboard shortcuts to target the right element

### Screenshot Workflow
1. Take screenshot: `DISPLAY=:1 scrot /tmp/screen.png`
2. Read it yourself: `read_file("/tmp/screen.png")` — this lets YOU see the screen
3. Send to user: `message(content="...", media=["/tmp/screen.png"])`
4. Always screenshot AFTER actions to verify results

### Gateway + GUI
- When running `nanobot gateway`, always start with `DISPLAY=:1` so Telegram/Discord agents can use GUI
- The gateway agent has its own context — it won't know about the display unless MEMORY.md says so
- Write important system info to MEMORY.md so all channels stay informed
