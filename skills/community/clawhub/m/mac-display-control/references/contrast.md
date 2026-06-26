# Contrast Control

VCP code: `0x12` | Range: 0–100

Contrast controls the difference between light and dark areas. Most displays ship at 50–75.
Lowering contrast can reduce eye strain; raising it makes text pop on bright content.

## Commands

### Apple Silicon (m1ddc)
```bash
m1ddc get contrast            # read current value
m1ddc set contrast 60         # set to 60
m1ddc chg contrast +5         # increase by 5
m1ddc chg contrast -5         # decrease by 5
```

### Intel (ddcctl)
```bash
ddcctl -d 1 -c ?              # read current value
ddcctl -d 1 -c 60             # set to 60
```

## Tips

- ⚠️ Some displays lock contrast when a color preset (sRGB, Movie, etc.) is active.
  Switch OSD to "Custom" / "User" color mode first.
- Contrast is less often scripted than brightness, but useful for switching between
  coding (lower) and media watching (higher) modes.
- Typical comfortable range: 50–70 for everyday use.