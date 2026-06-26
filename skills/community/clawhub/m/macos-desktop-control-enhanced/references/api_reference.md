# macOS Desktop Control Enhanced – API Reference

## Screenshot
- `screenshot([options])`
  - **Options**: `region` (geometry string `"x,y,w,h"`), `file_path` (default: `/tmp/screenshot.png`)
  - **Returns**: Path to saved screenshot image.

## Process Management
- `get_front_process()`
  - **Returns**: `{pid: <int>, bundle_id: <str>, name: <str>}` – info of frontmost process.
- `kill_process(pid)`
  - **Effect**: Terminates the process with the given PID.
- `launch_app(bundle_id)`
  - **Effect**: Opens the application identified by `bundle_id`.
- `terminate_app(bundle_id)`
  - **Effect**: Force‑closes the application identified by `bundle_id`.

## Clipboard
- `get_clipboard()`
  - **Returns**: Current clipboard text (string).
- `set_clipboard(text)`
  - **Effect**: Overwrites clipboard with `text`.

## System Information
- `get_system_info()`
  - **Returns**: `{os_version: <str>, battery: <str>}` – macOS version and battery level.

## Application Control
- `focus_app(bundle_id)`
  - **Effect**: Brings the app with the given `bundle_id` to the foreground.
- `terminate_app(bundle_id)`
  - **Effect**: Force‑closes the app with the given `bundle_id`.

## Mouse Control
- `move_mouse(x, y)`
  - **Effect**: Moves cursor to coordinates `(x, y)`.
- `click(x, y, button='left')`
  - **Effect**: Performs a mouse click at `(x, y)` with specified `button`.
- `drag(x1, y1, x2, y2, button='left')`
  - **Effect**: Drags from `(x1, y1)` to `(x2, y2)`.

## Keyboard Control
- `type_text(text)`
  - **Effect**: Types the given `text` via system keyboard.
- `press_key(key)`
  - **Effect**: Sends a single keyboard key event (key name or code).

---

*All functions are pure Python wrappers that invoke native macOS command‑line tools (`screencapture`, `osascript`, `pmset`, etc.) and therefore do not require additional binaries.*  