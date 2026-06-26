---
name: iaworker
description: "Intelligent Automation Worker — analyzes video/image streams and generates structured, real-time operating steps for physical tasks (debug, repair, assembly, inspection). Displays and speaks out step-by-step guidance using TTS. Use when: (1) User provides a video or image of a broken/damaged object (bike, car, appliance, etc.) and needs diagnosis and repair steps, (2) User wants guided step-by-step instructions for a physical task, (3) User wants real-time TTS spoken guidance alongside visual display, (4) User needs a structured workflow for analyzing physical problems and generating actionable steps."
---

# iaworker — Intelligent Automation Worker

Analyze video/image streams, diagnose physical problems, and generate structured step-by-step operating guidance. Deliver instructions both visually (displayed markdown) and audibly (TTS spoken aloud).

---

## Core Workflow

```
┌─────────────────────────────────────────────────────────────────────┐
│                        iaworker PROCESS                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  [1] RECEIVE INPUT                                                   │
│      Video file path, image path, or live camera frame              │
│           ↓                                                          │
│  [2] ANALYZE (video_analyzer.py)                                     │
│      - Extract key frames                                             │
│      - Identify objects, damage, components                           │
│      - Detect anomaly patterns (cracks, loose parts, fluid leaks)   │
│      - Classify task type (repair / assembly / inspection / debug)   │
│           ↓                                                          │
│  [3] GENERATE STEPS (step_engine.py)                                 │
│      - Build ordered, numbered action steps                           │
│      - Include tool requirements, safety warnings                   │
│      - Flag prerequisite steps (disconnect power, etc.)             │
│      - Estimate difficulty/time for each step                       │
│           ↓                                                          │
│  [4] DELIVER (speaker.py + display)                                  │
│      - Display formatted markdown step guide                         │
│      - Speak each step aloud via TTS                                  │
│      - Step-by-step progression (not all at once)                    │
│      - Wait for user confirmation before advancing (configurable)    │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Quick Start

### Analyze an image and get spoken steps

```bash
python scripts/video_analyzer.py \
  --input /path/to/image.jpg \
  --task repair \
  --lang en \
  --speak
```

### Analyze a video and get per-segment steps

```bash
python scripts/video_analyzer.py \
  --input /path/to/video.mp4 \
  --task debug \
  --lang en \
  --speak \
  --step-by-step
```

### Analyze from camera feed (live)

```bash
python scripts/video_analyzer.py \
  --input camera \
  --task inspection \
  --lang en \
  --speak \
  --live
```

---

## Scripts

### video_analyzer.py

Entry point. Analyzes visual input and triggers step generation.

```bash
python scripts/video_analyzer.py [options]
```

**Options:**

| Flag | Description | Default |
|------|-------------|---------|
| `--input PATH` | Image path, video path, or `camera` for live | Required |
| `--task TYPE` | `repair`, `debug`, `assembly`, `inspection`, `auto` | `auto` |
| `--lang CODE` | `en` or `zh` | `en` |
| `--speak` | Enable TTS for step output | Disabled |
| `--step-by-step` | Speak and display one step at a time, wait for confirmation | Sequential mode |
| `--live` | Live camera mode with continuous analysis | Off |
| `--output PATH` | Write steps to markdown file | None (console only) |
| `--frame-skip N` | Skip every N frames in video (speed up analysis) | 10 |

**Task auto-detection:**

- `repair` — Something is broken; find damage, suggest fixes
- `debug` — Something isn't working; trace fault to cause
- `assembly` — Something needs to be built/put together
- `inspection` — Check condition, report findings

### step_engine.py

Generates structured steps from analysis results.

```python
from step_engine import StepEngine

engine = StepEngine(lang="en")
steps = engine.generate(
    task_type="repair",
    objects=["wheel", "chain", "brake caliper"],
    anomalies=["chain loose", "brake pad worn"],
    context={"bike_type": "mountain"}
)

for step in steps:
    print(step["number"], step["title"])
    print(step["description"])
    print(f"[Tools: {step['tools']}] [Time: {step['time_estimate']}]")
    if step["safety_warning"]:
        print(f"⚠️  {step['safety_warning']}")
```

**Step object schema:**

```python
{
    "number": int,              # 1-based step number
    "title": str,               # Short action title
    "description": str,         # Detailed description
    "tools": list[str],         # Required tools
    "time_estimate": str,       # e.g. "5-10 min"
    "difficulty": str,          # "easy" | "medium" | "hard" | "expert"
    "safety_warning": str|null,# Warning text if any
    "prerequisite": bool,       # Must be done before others proceed
    "common_mistakes": list[str],# What to avoid
}
```

**Difficulty classification:**

| Level | Indicator |
|-------|-----------|
| `easy` | No special tools, minimal risk |
| `medium` | Basic tools, some disassembly |
| `hard` | Specialty tools, significant disassembly |
| `expert` | Professional tools, structural risk |

### speaker.py

Handles TTS output and markdown display.

```python
from speaker import Speaker

speaker = Speaker(lang="en", tts_enabled=True)

speaker.display_and_speak("Step 1: Inspect the chain tensioner")
speaker.display_steps([...steps...])
speaker.speak_only("Make sure to wear safety glasses.")
speaker.wait_for_user("Press Enter when ready to continue")
```

**Features:**

- **gtts** (Google TTS) — default, works out of the box
- **pyttsx3** — offline fallback
- Markdown rendering in terminal with `rich` library
- Per-step speak with configurable pacing
- Confirmation gating between steps (for `--step-by-step` mode)

---

## Step Generation Guidelines

Steps must follow this structure:

1. **Prerequisites** — Things that must be done first (disconnect power, secure object, etc.)
2. **Assessment** — Inspect and confirm the problem
3. **Preparation** — Gather tools, clear workspace
4. **Main actions** — Numbered, one clear action per step
5. **Verification** — Test that the fix/assembly worked
6. **Cleanup** — Put back together, tidy tools

**Rules:**

- Each step = one action. If it has "and", it's two steps.
- Always include a safety check step after anything involving power, hot parts, or fluids.
- Difficulty and time estimate must be realistic.
- Flag the most common mistakes for each step.

---

## Configuration

Config file: `scripts/config.yaml`

```yaml
tts:
  engine: "gtts"          # "gtts" or "pyttsx3"
  lang: "en"
  speed: 1.0              # 0.5 = slow, 2.0 = fast
  volume: 1.0             # 0.0 to 1.0

display:
  use_rich: true          # Pretty terminal output
  color: "cyan"           # Step highlight color
  show_icons: true        # Show ✅ ⚠️ 🔧 icons

analysis:
  default_task: "auto"
  frame_skip: 10
  confidence_threshold: 0.6

step_delivery:
  auto_speak: true
  wait_confirmation: false
  speak_difficulty: true
  speak_time_estimate: true
```

---

## Task Reference

### Bike Repair — Chain Adjustment

```
🔧 Tools: Hex keys (4mm, 5mm), chain tool, lubricant
⏱ Time: 15-25 min
⚠️ Safety: Flip bike first — chain tension releases can snap
```

1. Flip bike, rest on seat and handlebars
2. Inspect chain for stiff links, rust, kinks
3. Loosen rear axle bolts (5mm hex)
4. Adjust chain tension via horizontal dropouts
5. Check tension: 10-15mm deflection at midpoint
6. Re-tighten axle bolts
7. Lubricate if needed, wipe excess
8. Test ride

### Car Debug — Engine Won't Start

```
🔧 Tools: OBD2 scanner, multimeter, basic socket set
⏱ Time: 20-40 min (diagnosis first)
⚠️ Safety: Disable ignition, disconnect battery negative first
```

1. Check if fuel pump primes (turn key to ON, listen)
2. Test battery voltage (>12.4V idle, >13.5V running)
3. Connect OBD2 scanner, read fault codes
4. Inspect spark plugs for gap/damage
5. Check for crank/cam position sensor signals
6. Verify immobilizer status
7. Narrow to most likely cause, then address

### Generic Assembly — IKEA-style

```
🔧 Tools: Hex key (included), Phillips screwdriver, hammer
⏱ Time: varies
⚠️ Safety: Enlist a second person for large panels
```

1. Unpack and sort all hardware (count screws, dowels)
2. Lay out all panels, identify front/back
3. Pre-assemble sub-groups before final join
4. Hand-tighten all screws first
5. Use cardboard to protect floors
6. Final torque pass after 24h

---

## Troubleshooting

### "No audio output"
- Check if `gtts` is installed: `pip install gtts`
- Fallback: `engine: pyttsx3` in config (offline)
- On headless servers: set `DISPLAY` env var or use `pyttsx3`

### "Analysis is slow on video"
- Increase `--frame-skip` (e.g., `--frame-skip 30`)
- Use `--input camera --live` for real-time with throttled analysis

### "Steps are too generic"
- Provide more context in the initial prompt
- Use `--task repair` explicitly if auto-detect fails
- For specialized equipment, the LLM analysis quality depends on prompt specificity

### "OpenCV camera not found"
- Check camera index: `python scripts/video_analyzer.py --input camera --list-devices`
- Try `--input camera --camera-index 1` if default is wrong

---

## Extending for Specific Domains

iaworker ships with general-purpose analysis. To add domain-specific knowledge:

1. Create `references/domains/MYDOMAIN.md` with known failure modes and tool lists
2. In `step_engine.py`, add a `DOMAIN_HANDLERS` map that loads these
3. The step engine will then reference domain files when generating steps

Example domain file:

```markdown
# Domain: electric_bike

## Common Failures
- Motor controller overheating → reduce load, check ventilation
- Battery BMS cutout → reset via unplugging 30s
- Torque sensor miscalibration → re-zero via display menu

## Safety
- Never open motor housing — high voltage capacitors retain charge
- Battery must be removed before any repair
```
