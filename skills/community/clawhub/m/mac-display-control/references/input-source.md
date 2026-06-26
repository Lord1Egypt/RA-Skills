# Input Source Switching

VCP code: `0x60` | Type: Non-continuous (enum)

Switches the active input on your display — e.g. from HDMI to DisplayPort.
Useful if you share a display between two computers.

## Standard Input Source Values

| Value (decimal) | Value (hex) | Input |
|---|---|---|
| 1  | 0x01 | VGA-1 |
| 2  | 0x02 | VGA-2 |
| 3  | 0x03 | DVI-1 |
| 4  | 0x04 | DVI-2 |
| 15 | 0x0F | DisplayPort-1 |
| 16 | 0x10 | DisplayPort-2 |
| 17 | 0x11 | HDMI-1 |
| 18 | 0x12 | HDMI-2 |
| 27 | 0x1B | USB-C / Thunderbolt |

> ⚠️ These are standard MCCS values, but **displays often use non-standard codes**.
> Always probe your specific display first (see below).

## Probe Your Display's Input Codes

### Apple Silicon (m1ddc)
```bash
m1ddc get input               # read current input code
```

Then try switching and reading again to discover which codes your display uses.

### Intel (ddcctl)
```bash
ddcctl -d 1 -i ?              # read current input source
ddcctl -d 1 --get-input-source  # alternative on some versions
```

## Switch Input Commands

### Apple Silicon (m1ddc)
```bash
m1ddc set input 15            # switch to DisplayPort-1
m1ddc set input 17            # switch to HDMI-1
m1ddc set input 27            # switch to USB-C
```

### Intel (ddcctl)
```bash
ddcctl -d 1 -i 15             # switch to DisplayPort-1
ddcctl -d 1 -i 17             # switch to HDMI-1
```

## Two-Computer KVM Script

If you share a display between two Macs (or a Mac and a PC), script the switch:

**~/scripts/switch-to-mac.sh**
```bash
#!/bin/bash
# Switch display to USB-C (Mac Mini)
/opt/homebrew/bin/m1ddc set input 27
```

**~/scripts/switch-to-pc.sh**
```bash
#!/bin/bash
# Switch display to HDMI (PC)
/opt/homebrew/bin/m1ddc set input 17
```

## Tips

- ⚠️ Some displays only accept input-switch commands from the **currently active input**.
  If the command seems ignored, you may need to send it from the source you're switching *from*.
- After switching, the display may take 2–5 seconds to detect the new signal.
- Input codes vary by brand. LG, Dell, BenQ all use slightly different values.
  Always verify with `m1ddc get input` before scripting.