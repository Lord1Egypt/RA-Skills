# Brightness Control

VCP code: `0x10` | Range: 0–100

## Commands

### Apple Silicon (m1ddc)
```bash
m1ddc get luminance           # read current value
m1ddc set luminance 70        # set to 70
m1ddc chg luminance +10       # increase by 10
m1ddc chg luminance -10       # decrease by 10
```

### Intel (ddcctl)
```bash
ddcctl -d 1 -b ?              # read current value
ddcctl -d 1 -b 70             # set to 70
```

## Shell Scripts

**~/scripts/brightness-up.sh** (Apple Silicon)
```bash
#!/bin/bash
/opt/homebrew/bin/m1ddc chg luminance +10
```

**~/scripts/brightness-up.sh** (Intel)
```bash
#!/bin/bash
CURRENT=$(/usr/local/bin/ddcctl -d 1 -b ? 2>&1 | grep -o 'current: [0-9]*' | awk '{print $2}')
/usr/local/bin/ddcctl -d 1 -b $((CURRENT + 10))
```

**~/scripts/brightness-set.sh** (both — change tool as needed)
```bash
#!/bin/bash
# Usage: brightness-set.sh 70
/opt/homebrew/bin/m1ddc set luminance "${1:-50}"
```

## Tips

- Good daytime range: 70–100. Night range: 20–50.
- Combine with time-based cron presets (see SKILL.md Step 6).
- If brightness doesn't respond, Dynamic Contrast (DCR) may be enabled in OSD — disable it.