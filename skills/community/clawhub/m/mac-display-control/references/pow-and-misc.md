# Power & Miscellaneous Controls

## Display Power (VCP `0xD6`)

Turn the display panel on/off without cutting power to the device.

### Apple Silicon (m1ddc)
```bash
m1ddc set poweron 1           # wake / turn on
m1ddc set poweron 4           # standby (panel off, responds to signal)
m1ddc set poweron 5           # power off
```

### Intel (ddcctl)
```bash
ddcctl -d 1 -o 1              # power on
ddcctl -d 1 -o 4              # standby
ddcctl -d 1 -o 5              # power off
```

**Use case**: Script a "presentation mode" that turns off a secondary display when idle,
or wake it on demand without touching the physical button.

---

## Screen Orientation / Rotation (VCP `0xAA`)

| Value | Orientation |
|---|---|
| 1  | 0° (landscape) |
| 2  | 90° (portrait, rotated right) |
| 4  | 270° (portrait, rotated left) |

### Apple Silicon (m1ddc)
```bash
m1ddc get orientation
m1ddc set orientation 2       # rotate to portrait
m1ddc set orientation 1       # back to landscape
```

> ⚠️ Not all displays support software rotation via DDC. Most rely on the physical stand
> and macOS display settings instead. Try it — if no response, use System Settings → Displays → Rotation.

---

## OSD Language (VCP `0xCC`)

Change the language of the on-screen display menu.

```bash
m1ddc set osdlang 2           # English (common value; varies by brand)
```

---

## Restore Factory Defaults (VCP `0x04`)

Resets all display settings to factory state.

### Apple Silicon (m1ddc)
```bash
m1ddc set reset 1
```

### Intel (ddcctl)
```bash
ddcctl -d 1 --set-vcp 0x04 1
```

> ⚠️ This resets **everything** — brightness, contrast, color, input preferences.
> Use with caution. There is no undo.

---

## Discover All Supported Controls

Every display implements a different subset of DDC. Before scripting anything advanced,
probe what your display actually supports:

### Apple Silicon (m1ddc)
```bash
m1ddc display list
# m1ddc doesn't have a full capability dump; test controls individually
```

### Intel (ddcctl)
```bash
ddcctl -d 1 -p 1              # probe and print all supported VCP codes
```

This output tells you exactly which VCP codes work on your specific display.