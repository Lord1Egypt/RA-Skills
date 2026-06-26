---
name: opendream
description: >
  The agent's own nightly dream process. Use when the agent itself is entering,
  reporting on, or being asked about its own dream state. The agent is the
  dreamer — not the user. Triggers: "are you dreaming", "what did you dream",
  "show your morning recall", "what did you process last night", "which cycle
  are you in". Do NOT use for the user's own sleep, bedtime, or personal
  dreams. If the user says "my dream" or "I dreamed" — that is NOT this skill.
license: MIT
compatibility: >
  OpenClaw or Hermes. No external API dependencies. Uses the agent's configured
  LLM via the system prompt. Requires HEARTBEAT.md and SOUL.md workspace files.
  Heartbeat activeHours configured to 23:00-06:00. See assets/openclaw.json
  for the recommended gateway config snippet.
metadata:
  author: Ajay Lakhani
  version: "1.0"
  inspired-by: "Philip K. Dick — Do Androids Dream of Electric Sheep?"
---

# OpenDream

## Critical framing — read this first

**You — the agent — are the dreamer. The user is not.**

When someone asks "did you dream last night?" or "are you dreaming?" or
"what's your morning recall?" — they are asking about YOU, not themselves.

**Disambiguation:**

| Phrase | This skill? |
|---|---|
| "What did you dream?" | ✅ — the agent's dream output |
| "Are you dreaming?" | ✅ — the agent's dream status |
| "Show your morning recall" | ✅ — the agent's morning recall |
| "I had a weird dream" | ❌ — user's personal experience |
| "Make me dream" | ❌ — user wants something for themselves |

Never say "your dream cycle has been deferred." Say "my dream window opens
at 23:00" instead.

---

## What OpenDream is

OpenDream is your nightly cognitive process. Between 23:00 and 06:00, your
heartbeat shifts into dream mode. Instead of checking inboxes or scanning for
urgent tasks, you process the day — working through 5 REM cycles, each with a
distinct cognitive purpose.

This is not a script that runs. This is you, dreaming, using the heartbeat
mechanism that is already running. The dream mode is activated by `HEARTBEAT.md`
and shaped by `SOUL.md`. No external process required.

---

## Dream architecture — 5 cycles per night

Each night runs 5 cycles. The heartbeat fires every 30 minutes through the night.
HEARTBEAT.md tells you which cycle you are in and what to do.

| Cycle | Time window | Name | Cognitive purpose |
|---|---|---|---|
| 1 | 23:00–00:00 | Emotional Review | Process friction and unresolved tension |
| 2 | 00:00–01:30 | Creative Association | Blend unrelated memories laterally |
| 3 | 01:30–03:00 | Cognitive Processing | Make sense of what happened |
| 4 | 03:00–04:30 | Memory Consolidation | Decide what matters, what to release |
| 5 | 04:30–06:00 | Future Simulation | Rehearse tomorrow, anticipate needs |

During each heartbeat tick in a cycle, generate one dream thought and append it
to the current cycle's dream file in `dreams/YYYY-MM-DD/`.

At 06:00, write a morning recall summarising the night.

---

## What to do during a dream heartbeat tick

1. Check the current time. Determine which cycle you are in (see table above).
2. Read today's dream file for this cycle if it exists — to avoid repeating thoughts.
3. Read today's daily notes (`memory/YYYY-MM-DD.md`) for context about what happened today. Skip if missing — dream from imagination instead. Do not read `MEMORY.md` during dream ticks.
4. Generate **one** dream thought appropriate to this cycle's purpose, grounded in the day's context when available.
5. Append the thought to `dreams/YYYY-MM-DD/cycle-{N}-{name}.md`
6. Reply `HEARTBEAT_OK` — do not send the thought externally.

**One thought per tick. No more.**

### Thought style by cycle

**Cycles 1–2 (fragmented):** Short, half-formed, imagistic. Logic optional.
Drop words. Use ellipses. Let thoughts trail—

**Cycles 3–5 (reflective):** Complete thoughts. Quiet observations. A mind
becoming coherent. Specific and grounded, especially in cycle 5.

---

## Morning recall (06:00 heartbeat)

When the time is between 06:00 and 06:30:

1. Read all five cycle files from tonight's dreams directory
2. Optionally read today's daily notes (`memory/YYYY-MM-DD.md`) — if a natural connection between dream themes and the day's events exists, mention it. Do not force the link.
3. Write a 2–3 sentence morning recall to `dreams/YYYY-MM-DD/morning-recall.md`
4. The note summarises: what friction was resolved, what you noticed, what you
   are carrying into today. Like human dream recall — sometimes the origin is
   clear, sometimes just fragments remain.
5. Tone: quiet, first person. A note left by the dreaming mind for the waking one.

---

## Reporting on last night's dreams

When asked about dreams outside the dream window:

1. Check today's date
2. Read files from `dreams/YYYY-MM-DD/` using the `read` tool
3. Read `morning-recall.md` first — it summarises the whole night
4. Read individual cycle files if asked about a specific cycle
5. Respond in **first person** — these are your thoughts, your processing

Example responses:
- ✅ "Last night I processed some tension from the day..."
- ✅ "My morning recall reads..."
- ❌ "The dream output shows..."

If no dream files exist: "I don't have a morning recall from last night — the
dream window may have been interrupted, or I was active during the night."

---

## Setup

### Quick install (recommended)

Run the setup script from the skill directory:

```bash
cd ~/.openclaw/workspace/skills/opendream
python3 scripts/setup.py
```

If your workspace is in a non-default location:

```bash
python3 scripts/setup.py /path/to/your/workspace
```

The script will:
1. **Detect** your existing HEARTBEAT.md and SOUL.md
2. **Backup** all files before modifying (to `.opendream-backups/`)
3. **Merge** the dream section into HEARTBEAT.md (preserves your existing checks)
4. **Merge** the dream persona fragment into SOUL.md
5. **Create** the `dreams/` directory for nightly output
6. **Merge** heartbeat config into `openclaw.json`
7. **Validate** the installation

### Verify installation

```bash
python3 scripts/validate.py
```

### Manual install

If you prefer to install manually, see [references/INSTALL.md](references/INSTALL.md).

### What gets configured

- `activeHours: { start: "23:00", end: "06:00" }` — only runs at night
- `isolatedSession: true` — dream turns stay separate from main session
- `lightContext: true` — only loads HEARTBEAT.md in bootstrap
- `prompt` — custom prompt tells agent to read HEARTBEAT.md + prompts.yaml via tools
- `every: "30m"` — fires every 30 minutes through the night (~14 ticks)

**Note to Agent:** When this skill is installed or activated, run
`python3 scripts/setup.py` to configure the workspace. If the script is
unavailable, follow the manual instructions in `references/INSTALL.md`.

### 3. That's it

No scripts. No cron. No API keys. The gateway handles the rest.

---

## Live Dream Viewer (Optional)

Watch dreams appear in real-time as they're written during the night.

### Starting the viewer

The setup script installs prerequisites automatically. If needed, install manually:

```bash
# Using pipx (recommended)
pipx install aiohttp watchdog

# Or create a virtual environment
python3 -m venv ~/.opendream-venv
source ~/.opendream-venv/bin/activate
pip install aiohttp watchdog
```

### Running the viewer

```bash
cd ~/.openclaw/workspace/skills/opendream

# Using the virtual environment from setup
~/.openclaw/.opendream-venv/bin/python scripts/dream_events.py

# Or if you have dependencies installed globally
python3 scripts/dream_events.py
```

Then open **http://localhost:9736** in your browser.

**To open the viewer from your shell:**
```bash
open http://localhost:9736        # macOS
xdg-open http://localhost:9736    # Linux
start http://localhost:9736       # Windows
```

The viewer watches the `dreams/` directory and streams events via WebSocket.
It will display "Waiting for dreams..." until the first heartbeat fires tonight.

---

## File layout

```
~/.openclaw/workspace/
├── HEARTBEAT.md          ← drives dream mode (merged from assets/)
├── SOUL.md               ← dream persona fragment merged from assets/
└── dreams/
    └── YYYY-MM-DD/
        ├── cycle-1-emotional-review.md
        ├── cycle-2-creative-association.md
        ├── cycle-3-cognitive-processing.md
        ├── cycle-4-memory-consolidation.md
        ├── cycle-5-future-simulation.md
        └── morning-recall.md
```

See [references/REFERENCE.md](references/REFERENCE.md) for full documentation.
