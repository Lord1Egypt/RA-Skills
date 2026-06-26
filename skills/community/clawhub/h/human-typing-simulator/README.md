# human-type

> Type text into a browser like a real human — typos, backspaces, pauses, variable speed.

An [OpenClaw](https://github.com/openclaw/openclaw) skill + standalone CLI that generates a realistic **keystroke script** from any target string and plays it back in a browser with human-like timing.

---

## Install

```bash
npm install -g human-type-cli
```

Or run directly without installing:

```bash
npx human-type-cli run --text "Hello world" --duration 5
```

---

## Quick start

```bash
# Type "Hello, world!" over 6 seconds with default settings
human-type run --text "Hello, world!" --duration 6

# Type into a specific field (CSS selector)
human-type run \
  --text "My name is Alex and I'd like more info." \
  --duration 12 \
  --mistakes 25 \
  --pauses 20 \
  --selector "#contact-message"

# Preview the script without actually typing
human-type run --text "Preview me" --duration 5 --dry-run
```

---

## How it works

`human-type` doesn't just add random delays between keystrokes. It models how humans actually type:

1. **Adjacent-key typos** — wrong chars are picked from real QWERTY neighbors (so `e` becomes `w`, `r`, `d`, or `s` — not a random char)
2. **Backspace correction** — mistakes are deleted character-by-character before retyping
3. **Thinking pauses** — random hesitation gaps mid-sentence
4. **Speed jitter** — each keystroke has independent timing noise (0.4×–1.8× of average)
5. **Seeded reproducibility** — fix `--seed` for the exact same sequence every run

The final text produced is always exactly what you specified.

---

## Commands

### `run` — Type directly into the browser

```
human-type run [options]

  --text <string>       Final text to produce (required)
  --duration <seconds>  Total typing time (default: 10)
  --mistakes <0-100>    Typo rate as % (default: 20)
  --pauses <0-100>      Pause frequency as % (default: 15)
  --selector <css>      CSS selector to focus before typing
  --delay-start <ms>    Wait before first keystroke (default: 500)
  --seed <number>       Fix RNG for reproducible output
  --dry-run             Print script, don't type
  --cdp-url <url>       Chrome DevTools Protocol URL (default: http://127.0.0.1:18800)
```

### `generate` — Save a script to JSON

```
human-type generate --text "..." --output ./script.json [same options as run]
```

### `play` — Replay a saved script

```
human-type play ./script.json [--selector <css>] [--cdp-url <url>]
```

### `inspect` — Show stats about a script

```
human-type inspect ./script.json
```

Output:
```
  Target text  "Hello, world!"
  Events       47
  Keystrokes   39
  Mistakes     8  (21%)
  Pauses       5
  Total time   6.2s
  Avg WPM      48
  Seed         839204712
```

---

## Script format

The JSON event format is simple and portable — use it to drive any automation tool:

```json
[
  { "type": "type",   "ch": "H", "time": 0,    "duration": 195 },
  { "type": "type",   "ch": "e", "time": 195,  "duration": 210 },
  { "type": "type",   "ch": "p", "time": 405,  "duration": 180 },
  { "type": "delete",            "time": 585,  "duration": 145 },
  { "type": "type",   "ch": "l", "time": 730,  "duration": 220 },
  { "type": "pause",             "time": 950,  "duration": 480 },
  ...
]
```

| Field | Values | Description |
|---|---|---|
| `type` | `"type"` / `"delete"` / `"pause"` | Event kind |
| `ch` | character string | Key to press (only on `type` events) |
| `time` | ms integer | Offset from start |
| `duration` | ms integer | Gap until next event |

---

## Typical OpenClaw workflow

```bash
# 1. Open the page
openclaw browser open https://example.com/signup

# 2. Find the element refs
openclaw browser snapshot --interactive

# 3. Type like a human
human-type run \
  --text "Alexandra Chen" \
  --duration 4 \
  --mistakes 15 \
  --selector "input[name='name']"

# 4. Type email naturally
human-type run \
  --text "alex.chen@example.com" \
  --duration 6 \
  --mistakes 10 \
  --pauses 5 \
  --selector "input[type='email']"

# 5. Verify
openclaw browser snapshot --interactive
```

---

## Tips

| Goal | Setting |
|---|---|
| Natural adult typist | `--mistakes 15 --pauses 10 --duration` ~50 WPM |
| Fast typist, few errors | `--mistakes 5 --pauses 5` |
| Slow/careful | `--mistakes 30 --pauses 30` longer duration |
| Exact replay in tests | `--seed 12345` |
| Multi-field form | Run once per field with different `--selector` |

**WPM reference**: 40–70 WPM is average adult. At 50 WPM, 50 characters ≈ 10 seconds.

---

## Browser support

Requires a running Chromium-based browser accessible via CDP:

- **OpenClaw managed browser**: default is `http://127.0.0.1:18800`
- **Custom OpenClaw profile or remote browser**: pass `--cdp-url http://host:port`

The CLI uses `playwright-core` to attach over CDP. It does not launch its own browser and does not rely on OpenClaw's internal HTTP control routes.

---

## License

MIT
