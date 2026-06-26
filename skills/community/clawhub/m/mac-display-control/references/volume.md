# Volume Control (Built-in Display Speakers)

VCP code: `0x62` | Range: 0–100

Controls the audio output volume of a display's built-in speakers.
Only relevant if your display has built-in speakers AND you're using them as the audio output.

## Commands

### Apple Silicon (m1ddc)
```bash
m1ddc get volume              # read current value
m1ddc set volume 50           # set to 50
m1ddc chg volume +10          # increase by 10
m1ddc chg volume -10          # decrease by 10
m1ddc set volume 0            # mute
```

### Intel (ddcctl)
```bash
ddcctl -d 1 -v ?              # read current value
ddcctl -d 1 -v 50             # set to 50
```

## Mute Toggle Script

**~/scripts/display-mute-toggle.sh** (Apple Silicon)
```bash
#!/bin/bash
CURRENT=$(/opt/homebrew/bin/m1ddc get volume 2>&1 | grep -o '[0-9]*' | head -1)
if [ "$CURRENT" -gt 0 ]; then
  echo $CURRENT > /tmp/display_last_volume
  /opt/homebrew/bin/m1ddc set volume 0
else
  LAST=$(cat /tmp/display_last_volume 2>/dev/null || echo 50)
  /opt/homebrew/bin/m1ddc set volume $LAST
fi
```

## Tips

- This only works for the display's own speakers, not headphones or USB audio.
- If macOS audio output is set to a different device (e.g. Mac's speakers), this has no effect.
- Many users prefer controlling volume via macOS system audio — use DDC volume only if
  you specifically want to control the display speakers independently.