# Source Notes

These ClawHub skills were inspected before drafting `mac-gui-control`.

## Adopted ideas

- `mac-use`: screenshot -> OCR/numbered targets -> click -> verify loop; clipboard paste for reliable multilingual text entry; avoid typing secrets.
- `desktop-control-for-macos`: logical coordinate convention, Retina calibration, AI semantic targeting first, OCR/OpenCV fallbacks, PyAutoGUI failsafe.
- `mac-compute-use`: Accessibility/UI-tree MCP can be powerful for native apps, but should be optional because it adds Homebrew/MCP setup and permission burden.
- `mac-control`: practical keyboard navigation fallback for protected pages and OAuth dialogs; verify-before-click discipline.

## Rejected or downgraded ideas

- Machine-specific hardcoded paths such as `/Users/eason/...` and `/opt/homebrew/bin/cliclick` as the only path. This iMac is Intel; Homebrew tools may be in `/usr/local/bin`.
- Heavy standalone runtimes as the default path. `computer-use-macos` is useful but too large for a fast everyday skill.
- Large skills with many unrelated scripts, voice control, cron setup, QQ-specific senders, contributor ranking, and generated reports. Keep this skill focused on generic GUI primitives.
- Deep AppleScript UI scripting as the default click mechanism. It is brittle across apps and often needs Accessibility anyway.

## Local host observations

- `screencapture` works and returns 5120x2880 raw screenshots.
- Finder desktop bounds return 2560x1440, confirming a 2x logical-to-raw Retina scale.
- `System Events` process window inspection currently fails with Accessibility error `-1719`; grant Accessibility before relying on deep UI inspection.
- `cliclick` 5.1 installed successfully via Homebrew at `/usr/local/bin/cliclick`; it still needs Accessibility permission before real clicks/keystrokes will work reliably.
- PyAutoGUI 0.9.54 and PyObjC Vision/Quartz/AppKit 12.2 installed successfully for the default Homebrew Python 3.14.
- ImageMagick install failed on `libheif` 1.23.0 because Big Sur's Apple Clang lacks `std::ranges`; do not retry the same latest Homebrew formula blindly.
- `opencv-python` on Python 3.14 and Python 3.13 falls back to a long source build instead of a wheel. Avoid installing it casually on this host. Use `mac_gui.py locate-template`'s Pillow/numpy fallback or later find a compatible older wheel/Python runtime.
