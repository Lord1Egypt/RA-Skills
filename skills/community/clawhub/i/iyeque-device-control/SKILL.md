---
name: device-control
description: "Bounded local desktop controls for explicit requests: adjust volume or brightness, open an allowlisted application, or close an exact process. Use only when the user clearly asks to control the device."
license: MIT-0
metadata:
  openclaw:
    emoji: "🎛️"
    requires:
      bins: ["node"]
    version: "1.3.1"
---

# Bounded device control

Run `ctl.js` only for an explicit user request. It supports volume, brightness, opening a small safe allowlist of common applications, and closing an exact process name. It never accepts arbitrary shell commands, paths, shell metacharacters, or arbitrary application names.

```bash
node ctl.js --action set_volume --value 50
node ctl.js --action change_volume --value -10
node ctl.js --action set_brightness --value 75
node ctl.js --action open_app --app firefox
node ctl.js --action close_app --app firefox
```

Volume and brightness are 0–100; deltas are -100–100. Opening is limited to common applications such as Firefox, Chrome, Chromium, Edge, VS Code, VLC, Spotify, Calculator, Files, and Terminal. Unsupported platform utilities return an error without fallback execution. Closing uses exact process matching rather than broad patterns.

## Source and support

Source: https://github.com/iyeque/openclaw-skills/tree/main/skills/device-control

Report bugs and security concerns through the repository issue guidance.
