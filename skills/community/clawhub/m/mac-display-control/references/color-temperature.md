# Color Temperature & Color Presets

## Color Preset (VCP `0x14`) — Most Common Approach

Switches between named presets like sRGB, Warm, Cool, User.
This is the easiest way to change the "warmth" of the display.

### Standard Preset Values

| Value | Preset |
|---|---|
| 0x01 | sRGB |
| 0x04 | 5000 K (warm/paper white) |
| 0x05 | 6500 K (daylight — default for most displays) |
| 0x06 | 7500 K |
| 0x07 | 8200 K |
| 0x08 | 9300 K (cool/blue) |
| 0x0B | User 1 (custom) |
| 0x0C | User 2 (custom) |

> Values vary by display brand. Probe yours: `m1ddc get colorpreset` or check OSD presets.

### Apple Silicon (m1ddc)
```bash
m1ddc get colorpreset             # read current preset
m1ddc set colorpreset 5           # set to 6500K (daylight)
m1ddc set colorpreset 4           # set to 5000K (warm/night)
```

### Intel (ddcctl)
```bash
ddcctl -d 1 -m ?                  # read current preset
ddcctl -d 1 -m 5                  # set to 6500K
ddcctl -d 1 -m 4                  # set to warm
```

---

## RGB Gain (VCP `0x16`, `0x18`, `0x1A`) — Fine Colour Tuning

Adjusts Red, Green, Blue channels independently (0–100 each).
Useful for reducing blue light manually without Night Shift.

### Apple Silicon (m1ddc)
```bash
m1ddc set redgain 90
m1ddc set greengain 85
m1ddc set bluegain 70     # reduce blue for warmer, night-friendly image
```

### Intel (ddcctl)
```bash
ddcctl -d 1 -rg 90        # red gain
ddcctl -d 1 -gg 85        # green gain
ddcctl -d 1 -bg 70        # blue gain
```

---

## Night Mode Script (Warm + Dim)

Combines brightness reduction and blue reduction for comfortable evening use.

**~/scripts/night-mode.sh** (Apple Silicon)
```bash
#!/bin/bash
/opt/homebrew/bin/m1ddc set luminance 30
/opt/homebrew/bin/m1ddc set bluegain 65
/opt/homebrew/bin/m1ddc set greengain 85
/opt/homebrew/bin/m1ddc set redgain 95
```

**~/scripts/day-mode.sh** (Apple Silicon)
```bash
#!/bin/bash
/opt/homebrew/bin/m1ddc set luminance 80
/opt/homebrew/bin/m1ddc set bluegain 100
/opt/homebrew/bin/m1ddc set greengain 100
/opt/homebrew/bin/m1ddc set redgain 100
```

## Tips

- macOS **Night Shift** already does software blue-light filtering — DDC RGB gain does it
  in hardware, which is more effective and doesn't affect color-critical work.
- ⚠️ RGB gain only works when OSD color mode is set to "Custom" / "User". sRGB mode
  locks these values.
- Changes persist across power cycles (stored in display firmware).