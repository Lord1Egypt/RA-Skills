---
name: internet-time
description: "Get the current Swatch Internet Time in beats (@000–@999). Use when someone asks 'Internet time', 'Swatch beats', 'What is the beat time?', '/beats', or discusses Swatch time conversion, timezone translation."
version: 1.0.7
homepage: https://github.com/swatchtime
license: MIT
required_commands:
  - python3
required_environment_variables: []
required_privileges: none
metadata: {"hermes":{"emoji":"🕐","category":"lifestyle","platform":"Linux, macOS, Windows"},"required_binaries":["python3"]}
---

# Internet Time (Swatch Beats)

## ⚠️ Agent Instruction

**Output ONLY the beat time formatted as bold `@000` (three digits, zero-padded). No reasoning, no explanation, no inner monologue, no extra text. Just the bold beat time.**

Returns the current time in Swatch Internet Time — a decimal time system where the day is divided into 1000 beats. Each beat = 1 minute 26.4 seconds. No time zones, no daylight saving.

## Requirements

| Binary | Purpose |
|--------|---------|
| `python3` | Run the beat calculation script |

## Quick Reference

| User wants... | Do this |
|---------------|---------|
| Get current beat time | Run `skill run internet-time` or `internet-time` |
| Get beat time for a specific timestamp | Provide ISO timestamp: `python3 {baseDir}/scripts/get_swatch_time.py 2025-01-01T00:00:00Z` |
| Learn how beats are calculated | Read the Implementation section |

## Trigger Phrases (case-insensitive)

- "Internet time"
- "Swatch Internet Time"
- "What is the time in beats?"
- "How many beats is it?"
- "What is the current beat time?"
- "Beat time"
- "Current beats?"
- "Swatch beats"
- "Swatch beat time"
- "@ time"
- "Swatch time"
- "/beats"

## Output Format

**Only output the beat time formatted as bold `@000` (three digits, zero-padded).**

| Beat | Output |
|------|--------|
| 0    | **`@000`** |
| 6    | **`@006`** |
| 42   | **`@042`** |
| 483  | **`@483`** |
| 999  | **`@999`** |

Never output `@6`, `@42`, or any unpadded form. When the day rolls over, both beat 0 and beat 1000 are represented as **`@000`**.

No extra text, no explanation — just the bold beat time.

## Usage

```bash
internet-time
# **@483**
```

Or as a module:
```python
from internet_time import get_swatch_time
print(get_swatch_time())  # @483
```

## Timezone Conversion

When a user asks for the time in a specific location (e.g., "What is the time in California in beats?"):
1. Resolve the location to its IANA timezone (e.g., `America/Los_Angeles`)
2. Get the current time in that timezone as an ISO timestamp
3. Convert that timestamp to UTC
4. Apply the Swatch beat calculation (BMT = UTC+1)

The script accepts an optional ISO timestamp argument for this purpose.

## Implementation

Single-file Python module at `scripts/get_swatch_time.py`:

```python
#!/usr/bin/env python3
# get_swatch_time.py
# Single-file example that prints the current Swatch Internet Time to stdout
# Canonical definition: Biel = UTC+1 (fixed), no DST. One beat = 86.4 seconds.

from datetime import datetime, timezone, timedelta
import sys

def get_swatch_time(dt=None):
    # Use provided datetime or current UTC time
    if dt is None:
        now = datetime.now(timezone.utc)
    else:
        # Accept naive or aware datetimes; normalize to UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        now = dt.astimezone(timezone.utc)

    utc_seconds = now.hour * 3600 + now.minute * 60 + now.second
    biel_seconds = (utc_seconds + 3600) % 86400
    beat = int(biel_seconds // 86.4) % 1000
    return f"@{beat:03d}"

# Centibeat helper (safe rounding + wrap):
# raw = biel_seconds / 86.4
# rounded = round(raw * 100) / 100
# if rounded >= 1000:
#     rounded -= 1000
# display = f"{rounded:.2f}"

if __name__ == '__main__':
    # Optional: allow passing an ISO timestamp as first arg
    if len(sys.argv) > 1:
        t = datetime.fromisoformat(sys.argv[1].replace('Z', '+00:00'))
        print(get_swatch_time(t))
    else:
        print(get_swatch_time())

# Examples:
# From skill root: python3 scripts/get_swatch_time.py
# From workspace root: python3 skills/internet-time/scripts/get_swatch_time.py
# With timestamp: python3 skills/internet-time/scripts/get_swatch_time.py 2025-01-01T00:00:00Z
```

**Algorithm:**
1. Get current UTC time (or accept a datetime for testing)
2. Add 3600 seconds (1 hour) for Biel Mean Time = UTC+1, no DST
3. Modulo 86400 (seconds in a day) to wrap
4. Integer divide by 86.4 → beat (0–999)
5. Format as `@` + zero-padded 3 digits

## Error Handling

- If `python3` is not installed or not in PATH, the skill will fail to execute.
- The script validates input; invalid ISO timestamps will raise a Python exception.
- For best results, ensure the system has Python 3.6+ installed.

## Directory Structure

```
internet-time/
├── SKILL.md
└── scripts/
    └── get_swatch_time.py
```

## Reference

- Swatch Internet Time spec: https://www.swatch.com/en-us/internet-time
- Reference implementation: https://github.com/swatchtime/sample-code/blob/main/python/get_swatch_time.py
- BMT = UTC+1 (fixed, no DST)
- 1 beat = 86.4 seconds
- 1000 beats = 1 day

## Usage Notes

**Important:** The script path `scripts/get_swatch_time.py` shown above is **relative to the skill's directory**. When running the skill from ClawHub, the skill system handles locating and executing the script correctly.

If you are running the script manually from a cloned skill directory:
- Navigate to the skill root first: `cd skills/internet-time`
- Then run: `python3 scripts/get_swatch_time.py`
- Or reference it from the workspace root: `python3 skills/internet-time/scripts/get_swatch_time.py`

For normal use, prefer invoking the skill through ClawHub: `skill run internet-time` (or simply `internet-time` if the skill is installed and in your PATH).

## Security Disclaimers & Scanner False Positives

**What the scanner sees**: No subprocess calls, no network access, no file system writes.

**What is actually happening**: The skill performs only local datetime calculations and prints formatted output to stdout. It uses no external resources beyond the Python standard library.

**Why it matters**: This minimal attack surface confirms the skill is safe for execution in any environment.

<details>
<summary>📄 LICENSE.txt</summary>

```txt
MIT License

Copyright (c) 2026 Ken Dawson

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
</details>

<details>
<summary>📋 reference.json</summary>

```json
{
  "slug": "internet-time",
  "name": "Internet Time",
  "category": "lifestyle",
  "description": "Get the current Swatch Internet Time in beats (@000–@999).",
  "version": "1.0.7",
  "author": "Ken's Agents",
  "license": "MIT",
  "icon": "🕐",
  "tags": ["time", "swatch", "beats", "internet-time", "utility"],
  "platform": ["Linux", "macOS"],
  "required_binaries": ["python3"],
  "required_environment_variables": [],
  "required_privileges": "non-root",
  "triggers": [
    "internet time",
    "swatch internet time",
    "what is the time in beats",
    "how many beats is it",
    "what is the current beat time",
    "beat time",
    "current beats",
    "swatch beats",
    "swatch beat time",
    "@ time",
    "swatch time",
    "/beats"
  ]
}
```
</details>
