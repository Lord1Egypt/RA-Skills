---
name: "mac-gui-control"
description: "Control this macOS desktop via screenshots, AppleScript, mouse/keyboard automation, OCR/template matching, and verify loops."
---

# mac-gui-control

Use this skill to operate this Mac's GUI deliberately: perceive the screen, choose the least fragile control channel, act once, verify, and repeat. Prefer app-native APIs, shell commands, or browser automation when they solve the task cleanly; use GUI control for real desktop surfaces, native dialogs, canvas apps, Electron apps, and visual workflows.

## Machine Profile

This skill is tailored for the current host:

- macOS 11.6.5 Big Sur, Intel x86_64, iMac15,1.
- Built-in Retina 5K display: raw screenshots are 5120x2880.
- Logical desktop bounds are 2560x1440, so default scale is 2x.
- Currently available: `python3`, `osascript`, `screencapture`, Pillow, psutil, numpy, `cliclick`, PyAutoGUI, PyObjC Vision/Quartz/AppKit.
- Currently absent or degraded: OpenCV (`cv2`) and ImageMagick (`magick`). `locate-template` falls back to a Pillow/numpy matcher when OpenCV is unavailable.
- `System Events` deep window inspection and all pointer/keyboard injection require Accessibility permission for the runtime process.

Use logical coordinates for actions. The bundled helper captures logical screenshots by default so screenshot coordinates map to mouse coordinates.

## Setup Tiers

Tier 0 works immediately:

```bash
python3 {baseDir}/scripts/mac_gui.py env
python3 {baseDir}/scripts/mac_gui.py capture --output /tmp/mac_gui.png
python3 {baseDir}/scripts/mac_gui.py front-app
python3 {baseDir}/scripts/mac_gui.py activate --app "Google Chrome"
python3 {baseDir}/scripts/mac_gui.py key --combo command+l
python3 {baseDir}/scripts/mac_gui.py paste --text "hello"
```

Tier 1 adds reliable mouse control:

```bash
brew install cliclick
```

This host already has `cliclick` installed at `/usr/local/bin/cliclick`.

Then use:

```bash
python3 {baseDir}/scripts/mac_gui.py mouse click --x 500 --y 300
python3 {baseDir}/scripts/mac_gui.py mouse drag --x 400 --y 400 --to-x 900 --to-y 650
```

Tier 2 adds computer-vision helpers:

```bash
python3 -m pip install --user --break-system-packages pyautogui pyobjc-framework-Vision pyobjc-framework-Quartz pyobjc-framework-Cocoa numpy
```

This host already has PyAutoGUI, PyObjC Vision/Quartz/AppKit, Pillow, psutil, and numpy installed for the default `python3`.

OpenCV enables faster template matching when a compatible wheel exists. On this macOS 11 + Python 3.14 setup, `opencv-python` falls back to a long source build, so do not install it casually during interactive work. The helper's `locate-template` command uses OpenCV when present and otherwise falls back to a Pillow/numpy matcher.

Tier 3 is optional and heavier: install an MCP Accessibility/UI-tree server such as `mcp-server-macos-use` only when visual workflows are not enough and the task needs native accessibility-tree state.

## Permission Checklist

If screenshots are blank, grant Screen Recording to the host app or terminal process.

If clicks, keyboard shortcuts, or `System Events` window inspection fail with `not allowed assistive access` / `-1719`, grant Accessibility to the host app or terminal process, then restart that process.

Use these shortcuts:

```bash
open "x-apple.systempreferences:com.apple.preference.security?Privacy_ScreenCapture"
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Accessibility"
open "x-apple.systempreferences:com.apple.preference.security?Privacy_Automation"
```

## Control Ladder

Choose the highest reliable layer available:

1. Direct CLI/API/file operation. Do not use GUI when a stable local command does the job.
2. Browser automation for ordinary web pages when OpenClaw browser tools can inspect DOM or snapshots.
3. AppleScript app/window semantics: open, activate, get front app, get window bounds/title.
4. Accessibility/UI-tree MCP if installed and the app exposes useful UI elements.
5. Screenshot-guided semantic vision: capture, crop, ask the model to return structured `{found,x,y,confidence,reason}`.
6. OCR text targeting when the label is visible and unique.
7. Template matching when the target icon/button is stable: OpenCV if installed, otherwise Pillow/numpy fallback.
8. Manual coordinate click only after a screenshot and preferably inside a bounded region.
9. Keyboard navigation (`tab`, `shift+tab`, `return`, `escape`) when mouse injection is ignored, especially OAuth/login/protected dialogs.

## Core Loop

Always follow this loop for GUI tasks:

1. Activate or open the target app.
2. Capture a fresh logical screenshot.
3. Inspect the screenshot directly before acting.
4. Choose a target using the least fragile method available.
5. Act once.
6. Capture again and verify the expected change.
7. Continue or recover.

For externally visible actions, such as sending messages, submitting forms, payments, deletions, public posts, or account changes, stop before the final submit/send/delete unless the user explicitly authorized that exact action.

## Helper Commands

Use the bundled helper from the skill directory.

Environment and coordinates:

```bash
python3 {baseDir}/scripts/mac_gui.py env
python3 {baseDir}/scripts/mac_gui.py capture --output /tmp/mac_gui.png
python3 {baseDir}/scripts/mac_gui.py capture --raw --output /tmp/mac_gui_raw.png
python3 {baseDir}/scripts/mac_gui.py front-app
python3 {baseDir}/scripts/mac_gui.py bounds --app "Google Chrome"
```

App and keyboard control:

```bash
python3 {baseDir}/scripts/mac_gui.py activate --app "Google Chrome"
python3 {baseDir}/scripts/mac_gui.py key --combo command+l
python3 {baseDir}/scripts/mac_gui.py key --combo return
python3 {baseDir}/scripts/mac_gui.py paste --text "text to paste"
printf 'multi\nline' | python3 {baseDir}/scripts/mac_gui.py paste --stdin
```

Mouse control after `cliclick` or `pyautogui` is available:

```bash
python3 {baseDir}/scripts/mac_gui.py mouse position
python3 {baseDir}/scripts/mac_gui.py mouse move --x 500 --y 300
python3 {baseDir}/scripts/mac_gui.py mouse click --x 500 --y 300
python3 {baseDir}/scripts/mac_gui.py mouse double --x 500 --y 300
python3 {baseDir}/scripts/mac_gui.py mouse right --x 500 --y 300
python3 {baseDir}/scripts/mac_gui.py mouse drag --x 500 --y 300 --to-x 900 --to-y 500
```

Template matching:

```bash
python3 {baseDir}/scripts/mac_gui.py locate-template --image /tmp/mac_gui.png --template /tmp/button.png --threshold 0.86
```

If OpenCV is absent, the command uses the Pillow/numpy fallback. Use a smaller crop and a larger `--step` for speed, for example `--step 4`, when searching a large screenshot.

The helper prints JSON for machine-readable chaining.

## Vision Targeting Contract

When using model vision on a screenshot or crop, require compact JSON before clicking:

```json
{"found": true, "x": 742, "y": 681, "confidence": "high", "reason": "lower-right Queue button"}
```

Only click when `found=true` and confidence is high enough for the risk of the action. If confidence is medium, move/crop/verify first. If confidence is low or false, do not click.

Prefer cropping to a small relevant region before asking for a coordinate. Smaller screenshots reduce ambiguity and are faster to inspect.

## Text Entry

Use clipboard paste for normal text, especially Chinese, Japanese, mixed-language prompts, filenames, and long prompts. Per-key simulated typing is slower and can break under IME input methods.

Default paste flow:

1. Click the verified input field.
2. Paste with `mac_gui.py paste`.
3. Verify the text visually if it matters.
4. Press Return only when the action is safe or authorized.

Do not type passwords, tokens, or secrets through GUI automation unless the user explicitly asks and the target context is trusted.

## Coordinates

Default coordinate convention:

- `capture` writes logical screenshots sized to the desktop coordinate system, normally 2560x1440 on this iMac.
- Mouse actions use logical coordinates.
- Raw `screencapture` output is 5120x2880 on this 5K Retina display; use `--raw` only when preserving raw pixels matters.
- If mixing raw screenshots and mouse actions, divide raw coordinates by the detected scale factor before clicking.

## Recovery

If an action fails:

- Capture again before repeating.
- Check whether the wrong window is frontmost.
- Use `bounds` and `front-app` to confirm target state.
- Prefer keyboard navigation if clicks are ignored.
- Re-open permissions settings if `System Events` or mouse control reports Accessibility errors.
- Abort pointer automation immediately by moving the mouse to the top-left corner when PyAutoGUI is the backend.

## Source Notes

Read `references/source-notes.md` when revising this skill or deciding whether to add heavier dependencies. It summarizes which ClawHub skills informed this design and what was intentionally rejected.
