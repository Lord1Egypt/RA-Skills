---
name: openclawpanel
description: Control an OpenClaw LED panel (64x32 HUB75 on ESP32-S3) over HTTP — display text, graphics, shapes, play sounds, and read status.
metadata: {"openclaw":{"emoji":"💡","requires":{"bins":["curl"],"env":["OPENCLAW_PANEL_IP"]},"primaryEnv":"OPENCLAW_PANEL_IP"}}
user-invocable: true
---

# OpenClaw Panel

Control an OpenClaw LED panel (64x32 pixels, RGB565) connected to your local network via HTTP.

## Connection

The panel runs an HTTP server on port 80. Base URL: `http://${OPENCLAW_PANEL_IP}`.
Use `curl -s` with `-H "Content-Type: application/json"` for all POST requests.

## Display specs

- Resolution: 64 wide x 32 tall pixels
- Color format: RGB565 as hex string (e.g. `"0xF800"`) or HTML hex (`"#FF0000"`)
- Coordinates: (0,0) is top-left, (63,31) is bottom-right
- Fonts (name → size): `arial_20` (largest), `arial_18`, `arial_16`, `mono_18`, `mono_12`, `5x7`, `4x6` (smallest)
- Common colors: `"0xF800"` red, `"0x07E0"` green, `"0x001F"` blue, `"0xFFE0"` yellow, `"0xFFFF"` white, `"0x0000"` black, `"#FF6600"` orange

## Endpoints

### Display drawing

**POST /api/display/text** — Show text.
```json
{"text": "Hello", "x": 0, "y": 16, "color": "0x07E0", "font": "arial_20", "align_right": false, "swap": true}
```
All fields except `text` are optional (defaults: x=0, y=0, color=white, font=mono_12, align_right=false, swap=true).

**POST /api/display/number** — Show a formatted number (large values auto-format: 1000000 → "1 M").
```json
{"value": 64770, "x": 0, "y": 20, "color": "0xFFFF", "font": "arial_20", "align_right": false, "swap": true}
```

**POST /api/display/clear** — Clear the display to black. No body needed.

**POST /api/display/pixel** — Draw pixels. **Limit: ~400 pixels per call** — larger payloads cause "Invalid JSON" on the ESP32. For filled areas, prefer `rect`, `circle`, or `line` endpoints instead.
```json
{"pixels": [{"x": 10, "y": 5, "color": "0xF800"}, {"x": 11, "y": 5, "color": "0x07E0"}], "swap": true}
```

**POST /api/display/line** — Draw a line between two points (Bresenham).
```json
{"x0": 0, "y0": 0, "x1": 63, "y1": 31, "color": "0xF800", "swap": true}
```
All fields except coordinates are optional (defaults: color=white, swap=true).

**POST /api/display/rect** — Draw a rectangle.
```json
{"x": 0, "y": 0, "w": 64, "h": 32, "color": "0x001F", "fill": true, "swap": true}
```
`fill` defaults to true. Set false for outline only.

**POST /api/display/circle** — Draw a circle.
```json
{"cx": 32, "cy": 16, "r": 10, "color": "0xFFE0", "fill": false, "swap": true}
```
`fill` defaults to false (outline). Set true for filled circle.

**POST /api/display/graph** — Draw a line graph.
```json
{"values": [1.0, 3.5, 2.0, 7.0, 5.5], "x": 0, "y": 8, "w": 64, "h": 24, "color_line": "0x07E0", "color_fill": "0x07E0", "fill": true, "swap": true}
```
Values are auto-scaled to fit the height. `fill` fills the area under the line.

**POST /api/display/panel** — Show a full dashboard panel (label + value + percentage + graph).
```json
{"label": "BTC", "value": 64770, "percent": 3.5, "values": [60000, 61000, 63000, 64770], "color_line": "0xFFE0", "color_fill": "0xFFE0", "fill": true, "dissolve": true}
```
This clears the screen and draws a complete panel. `dissolve` enables a fade transition.

**POST /api/display/gif** — Play the built-in animated GIF. No body needed.
Plays the built-in OpenClaw logo animation. Requires lock + clear before calling, otherwise nothing appears.
```
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/lock
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/clear
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/gif
```

**POST /api/display/bitmap** — Draw a raw RGB565 bitmap. Body is raw binary (w*h*2 bytes). Dimensions via query params.
```
POST /api/display/bitmap?x=0&y=0&w=16&h=8&swap=1
Content-Type: application/octet-stream
Body: <raw RGB565 bytes, little-endian, row-major>
```
Max size: 64x32 (4096 bytes). Each pixel is 2 bytes RGB565.

**POST /api/display/dissolve** — Smooth fade transition from current display to the back buffer.
```json
{"steps": 10, "ms_per_step": 30}
```
Draw new content with `"swap": false` first, then call dissolve to transition. Both fields optional (defaults: steps=10, ms_per_step=30).

**POST /api/display/brightness** — Set display brightness.
```json
{"value": 80}
```
Range: 0 (off) to 100 (max). Persists across reboots.

**GET /api/display/framebuffer** — Returns 4096 bytes of raw RGB565 binary data (64x32 pixels, row-major).

### Display control

**POST /api/display/lock** — Take exclusive control of the display. Pauses the normal panel timeline. No body needed. Auto-unlocks after 30 seconds of inactivity.

**POST /api/display/unlock** — Release control back to the normal timeline. No body needed.

**POST /api/view_panel** — Force a specific timeline panel to show.
```json
{"index": 0}
```
This also unlocks the display if it was locked.

### Sound

**POST /api/sound/play** — Play a built-in sound. Blocks until playback finishes.
```json
{"name": "coin"}
```
Available sounds: `order` (cash register), `coin` (Mario coin), `epicwin` (victory fanfare), `youwin` (short win).

**POST /api/sound/wav** — Upload and play a custom WAV file. Body is raw WAV data (max 64 KB). Non-blocking (plays in background).
```
POST /api/sound/wav
Content-Type: application/octet-stream
Body: <raw WAV file bytes>
```
**WAV format requirements (strict):**
- Format: RIFF WAV, uncompressed PCM only (format tag = 1). No MP3, OGG, ADPCM, or other codecs.
- Bit depth: **16-bit only** (8-bit is NOT supported and will be rejected).
- Channels: Mono (1ch) or Stereo (2ch). **Mono recommended** — uses half the size.
- Sample rate: Any (the hardware reinitializes to match). **11025 Hz recommended** — higher rates (22050/44100) often cause "No memory" errors on the ESP32. 11025 Hz gives the best reliability and allows longer clips.
- Max file size: **64 KB** (65536 bytes including headers).
- Max duration at 44100 Hz mono: ~0.74s. At 22050 Hz mono: ~1.48s. At 11025 Hz mono: ~2.96s.

To convert any audio file to a compatible WAV, use ffmpeg:
```bash
ffmpeg -i input.mp3 -ar 11025 -ac 1 -sample_fmt s16 -t 2.9 output.wav
```

**GET /api/sound/list** — Returns JSON array of built-in sound names.
Response: `["order","coin","epicwin","youwin"]`

**POST /api/sound/volume** — Set speaker volume. Persists across reboots.
```json
{"value": 50}
```
Range: 0 (mute) to 100 (max).

**GET /api/sound/status** — Returns current volume and mute state.
Response: `{"volume": 50, "muted": false}`

### Status

**GET /api/status** — Returns device info.
Response: `{"version": "1.7.1", "ip": "192.168.1.50", "brightness": 80, "volume": 50, "display": {"w": 64, "h": 32}, "ws_connected": true, "api_locked": false}`

## The `swap` parameter

Most draw endpoints accept `"swap": true|false` (default: true).
- `true`: the drawing appears on screen immediately after the call.
- `false`: the drawing is buffered but not shown yet. Use this to compose multiple elements before displaying them all at once. Send a final call with `"swap": true` to show everything.

## Workflow

1. **To show something temporarily**, use lock/draw/unlock:
   ```
   POST /api/display/lock
   POST /api/display/clear
   POST /api/display/text  {"text":"HELLO","x":5,"y":20,"color":"0x07E0","font":"arial_20"}
   ... (display stays until unlock or 30s timeout)
   POST /api/display/unlock
   ```

2. **To compose a scene** (multiple elements), use swap=false for all but the last:
   ```
   POST /api/display/lock
   POST /api/display/clear
   POST /api/display/rect   {"x":0,"y":0,"w":64,"h":10,"color":"0x001F","fill":true,"swap":false}
   POST /api/display/text   {"text":"BTC","x":2,"y":8,"color":"0xFFFF","font":"4x6","swap":false}
   POST /api/display/text   {"text":"64,770","x":2,"y":24,"color":"0xFFE0","font":"arial_16","swap":true}
   POST /api/display/unlock
   ```
   Always use `"swap": false` on every element except the very last one. This prevents flicker and ensures the entire scene appears at once.

3. **To show something for a fixed duration** (auto-unlock pattern):
   ```
   POST /api/display/lock
   POST /api/display/clear
   POST /api/display/text  {"text":"ALERT","x":4,"y":22,"color":"0xF800","font":"arial_20"}
   sleep 5
   POST /api/display/unlock
   ```
   Use this when the user wants to flash a message briefly. Always unlock after the sleep.

4. **For sounds**, just call directly (no lock needed):
   ```
   POST /api/sound/play  {"name":"coin"}
   ```

5. **To return to normal operation**: call unlock, or use view_panel to jump to a specific dashboard panel.

## Guardrails

- **Always call POST /api/display/lock before any drawing operation. No exceptions — even for quick single draw calls.**
- Always unlock the display when done. Never leave it locked indefinitely.
- The display is tiny (64x32 pixels). Keep text very short: ~5-6 chars max for arial_20, ~10 chars for mono_12, ~16 chars for 4x6.
- Prefer `mono_12` or `4x6` for informational text — they are more legible than large fonts on a 64x32 display. Reserve `arial_20` for single words or short numbers.
- The y coordinate in text is the baseline (bottom of text), not the top. For arial_20, use y=20-28. For 4x6, use y=6-30.
- When drawing a filled circle with an outline, draw the filled circle first, then the outline on top. On small screens, an outline drawn under a fill can be completely hidden.
- Do not set brightness or volume outside 0-100.
- If the user says "reset", "stop", or "back to normal", call POST /api/display/unlock.
- Check GET /api/status first if unsure whether the panel is reachable.

## Real-world calibration (64x32 panel)

Font sizing for typical short text (4-6 chars):
- `arial_20` — too large for most use cases, text overflows or looks crowded
- `arial_16` — still large, ok for 1-3 chars
- `mono_12` — good default for short words (4-6 chars)
- `5x7`, `4x6` — use for longer strings or when showing multiple lines

Centering tips for `mono_12`:
- Vertical center: y≈12
- Horizontal: for a 4-char word (~6px/char), x≈18 centers on 64px wide display
- When in doubt, start at x=15-20, y=12 and adjust based on feedback

## Examples

User: "Show HELLO in green on the panel"
```
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/lock
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/clear
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/text -H "Content-Type: application/json" -d '{"text":"HELLO","x":18,"y":12,"color":"0x07E0","font":"mono_12"}'
```
Then after a few seconds: `curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/unlock`
Note: arial_20 is too large for 5-char words on a 64x32 display. mono_12 at y=12 centers vertically.

User: "Play the coin sound"
```
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/sound/play -H "Content-Type: application/json" -d '{"name":"coin"}'
```

User: "Draw a red circle in the center"
```
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/lock
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/clear
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/circle -H "Content-Type: application/json" -d '{"cx":32,"cy":16,"r":12,"color":"0xF800","fill":true}'
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/unlock
```

User: "Show Bitcoin at 64,770 with a chart"
```
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/lock
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/panel -H "Content-Type: application/json" -d '{"label":"BTC","value":64770,"percent":2.3,"values":[60000,61500,63000,64770],"color_line":"0xFFE0","color_fill":"0xFFE0","fill":true,"dissolve":true}'
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/unlock
```

User: "Set brightness to 30%"
```
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/brightness -H "Content-Type: application/json" -d '{"value":30}'
```

User: "Draw a diagonal red line"
```
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/lock
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/clear
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/line -H "Content-Type: application/json" -d '{"x0":0,"y0":0,"x1":63,"y1":31,"color":"0xF800"}'
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/unlock
```

User: "Smooth transition to new content"
```
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/lock
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/clear
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/text -H "Content-Type: application/json" -d '{"text":"NEW","x":10,"y":22,"color":"0x07E0","font":"arial_20","swap":false}'
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/dissolve -H "Content-Type: application/json" -d '{"steps":15,"ms_per_step":40}'
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/unlock
```

User: "Play a custom sound" (requires a local WAV file)
```
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/sound/wav --data-binary @mysound.wav
```

User: "What sounds are available?"
```
curl -s http://$OPENCLAW_PANEL_IP/api/sound/list
```

User: "Back to normal" / "Reset the panel"
```
curl -s -X POST http://$OPENCLAW_PANEL_IP/api/display/unlock
```
