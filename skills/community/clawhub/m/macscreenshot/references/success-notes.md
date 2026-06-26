# screenshot skill - success notes

## Confirmed successful path

Environment:
- macOS built-in tools only
- No extra screenshot software required
- No Python Quartz dependency required

Working sequence:
1. Use inline Swift to call `CGWindowListCopyWindowInfo`
2. Filter windows by `owner` and `name`
3. Read `kCGWindowNumber` as the window ID
4. Confirm `kCGWindowSharingState == 1` when possible
5. Run `screencapture -x -l <windowId> <output>`

## Real-world notes from WeChat capture

- App matched: `WeChat`
- A successful capture used a window entry like:
  - `id = 207`
  - `owner = WeChat`
  - `name = WeChat`
  - `sharing = 1`
- This was sufficient for `screencapture -l 207` to produce a PNG.

## Failure modes observed

### Python route failed

`ModuleNotFoundError: No module named 'Quartz'`

Interpretation:
- pyobjc / Quartz bindings are not guaranteed to exist
- Do not assume Python can enumerate macOS windows

### AppleScript AX window route failed

`Can't get attribute "AXWindowNumber"`

Interpretation:
- Some apps do not expose a usable `AXWindowNumber`
- Accessibility inspection is not a reliable way to obtain the screenshot window ID

### Accessibility denied

`osascript is not allowed assistive access`

Interpretation:
- Only relevant if using `System Events`
- Avoid this dependency when possible

## Recommendation

Prefer Swift + CoreGraphics first. Only mention Accessibility permissions when a task explicitly requires `System Events` or other UI scripting.
