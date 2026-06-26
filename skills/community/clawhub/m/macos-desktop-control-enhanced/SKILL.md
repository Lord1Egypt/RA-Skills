---
name: macos-desktop-control-enhanced
description: macOS Desktop Control Enhanced provides system-wide desktop automation on macOS, including screenshot capture, process management, clipboard operations, system information, application control (open/close), and direct mouse, keyboard, and screen interaction. Use this skill when you need to programmatically control or query the macOS desktop environment.
---

# When to Use This Skill

- You need to capture the screen or a region programmatically.
- You need to query or control running processes.
- You need to read or modify the clipboard content.
- You need to retrieve system information (e.g., battery level, OS version).
- You need to open, focus, or close applications by bundle ID.
- You need to move the mouse, click, drag, or simulate keyboard input.
- You need to integrate macOS desktop automation into larger workflows (e.g., testing, data collection, accessibility).

# Overview

macOS Desktop Control Enhanced offers the following core capabilities:

## 1. Screenshot
- `screenshot([options])` – Capture the entire screen or a specified region; returns image path.

## 2. Process Management
- `get_front_process()` – Returns information about the currently frontmost process.
- `kill_process(pid)` – Terminates the process with the given PID.
- `launch_app(bundle_id)` – Launches an application identified by its bundle ID.

## 3. Clipboard
- `get_clipboard()` – Retrieves current clipboard text.
- `set_clipboard(text)` – Overwrites the clipboard with the given text.

## 4. System Information
- `get_system_info()` – Returns a dictionary with macOS version, battery level, and other relevant system metrics.

## 5. Application Control
- `focus_app(bundle_id)` – Brings the specified application to the foreground.
- `terminate_app(bundle_id)` – Force‑closes the application with the given bundle ID.

## 6. Mouse Control
- `move_mouse(x, y)` – Moves the cursor to the given screen coordinates.
- `click(x, y, button='left')` – Performs a mouse click at the given coordinates.
- `drag(x1, y1, x2, y2, button='left')` – Drags from (x1, y1) to (x2, y2).

## 7. Keyboard Control
- `type_text(text)` – Types the given string using the system keyboard.
- `press_key(key)` – Sends a single keyboard key event.

# Structure

This skill follows a **Capabilities‑Based** structure, grouping functionality by core features. Each capability section lists the available functions, their purpose, and brief usage notes.

# References

- `references/api_reference.md` – Complete function signatures, parameter details, and return values.
- `scripts/example_mouse.py` – Sample Python script demonstrating mouse movement and clicking.
- `assets/example_asset.png` – Example asset showing a captured screenshot.

# License

MIT‑0 (Free to use, modify, and redistribute. No attribution required.)