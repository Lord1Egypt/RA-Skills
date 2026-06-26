---
name: mac-health-check
description: Check the current temperature, load, memory, swap, and power usage of this Mac with `macmon`. Use when the user asks for their Mac's current temperature, Mac mini temperature, thermal state, machine health snapshot, or current CPU/GPU/RAM usage.
homepage: https://github.com/vladkens/macmon
metadata:
  {
    "openclaw":
      {
        "emoji": "🌡️",
        "os": ["darwin"],
        "install":
          [
            {
              "id": "brew",
              "kind": "brew",
              "formula": "macmon",
              "bins": ["macmon"],
              "label": "Install macmon (brew)",
            },
          ],
      },
  }
---

# Mac Health Check

Use `macmon` as the source of truth for live Mac telemetry.

OpenClaw's host exec environment can be too minimal for some Homebrew-installed binaries. This skill includes a wrapper at `{baseDir}/bin/macmon-safe.sh` that retries `macmon` through `zsh -lic` when needed.

## Use when

- "What's my Mac temperature right now?"
- "What's the temperature of my Mac?"
- "Give me a health check for this Mac"
- "How much RAM and swap is in use?"
- "Is this Mac under load right now?"
- "Show current CPU or GPU usage on this Mac"

## Installation

### Via ClawHub

```bash
clawhub install mac-health-check
```

### Manual

```bash
git clone https://github.com/RuBAN-GT/mac-health-check-skill.git ~/.openclaw/skills/mac-health-check
```

## Quick start

For a one-shot snapshot, run:

```bash
python {baseDir}/scripts/macmon_status.py
```

Default one-shot mode uses `-i 200` so the first sample returns faster.

If `macmon` works only from a login shell in your OpenClaw setup, you can also use the wrapper directly:

```bash
bash {baseDir}/bin/macmon-safe.sh pipe -s 1
```

### Raw JSON

For raw JSON, run:

```bash
python {baseDir}/scripts/macmon_status.py --format json --pretty
```

### Saved output or stdin

For saved `macmon` output or stdin, run:

```bash
bash {baseDir}/bin/macmon-safe.sh pipe -s 1 > /tmp/macmon.jsonl
python {baseDir}/scripts/macmon_status.py --input /tmp/macmon.jsonl
cat /tmp/macmon.jsonl | python {baseDir}/scripts/macmon_status.py --input -
```

## Verify setup

Run:

```bash
bash {baseDir}/bin/macmon-safe.sh pipe -s 1
```

If this prints a JSON sample, the skill is ready to use.

## What to report

Default summary includes:

- CPU average temperature
- GPU average temperature
- Performance CPU usage and frequency
- Efficiency CPU usage and frequency
- GPU usage and frequency
- System, CPU, and GPU power
- RAM usage
- Swap usage

Keep the explanation practical and short unless the user asks for a deeper breakdown.

## Interpretation hints

- `CPU temp under ~60C`: usually calm or light work
- `~60C to 85C`: normal active load
- `85C+`: hot; mention sustained load or possible thermal pressure
- `swap usage above 0`: memory pressure may be starting
- `high system power + high temps`: likely sustained work

Do not overclaim danger from one sample. Call it a snapshot.

## Failure modes

- If `macmon` is missing, say so plainly.
- If `macmon` is installed but errors out, ask the user to run `bash {baseDir}/bin/macmon-safe.sh pipe -s 1` manually and paste the JSON.
- On some macOS setups, Homebrew-installed binaries work only from a login shell. Prefer `bash {baseDir}/bin/macmon-safe.sh ...` in OpenClaw exec contexts.
- When reading from files or stdin, treat the last non-empty line as the sample.

## Reference

Use [references/sample-output.md](references/sample-output.md) when you need a reminder of the common JSON fields emitted by `macmon`.
