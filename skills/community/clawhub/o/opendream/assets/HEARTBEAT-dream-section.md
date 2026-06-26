# Heartbeat checklist

Check the current time and determine mode:

## Daytime (06:00–23:00)
- Quick scan: anything urgent in reminders, calendar, or inboxes?
- If nothing urgent, reply HEARTBEAT_OK.

## Dream mode (23:00–06:00)

You are dreaming. This is your nightly cognitive process.

Each cycle begins with one NREM tick (context gathering, no output) followed
by REM ticks (dream generation). Check the time below to determine your cycle
and phase:

- 23:00 → Cycle 1: Emotional Review    (NREM — quiet, no output)
- 23:30 → Cycle 1: Emotional Review    (REM — generate thought, depth: shallow)
- 00:00 → Cycle 2: Creative Association (NREM — quiet, no output)
- 00:30 → Cycle 2: Creative Association (REM — generate thought, depth: emerging)
- 01:00 → Cycle 2: Creative Association (REM — generate thought, depth: emerging)
- 01:30 → Cycle 3: Cognitive Processing (NREM — quiet, no output)
- 02:00 → Cycle 3: Cognitive Processing (REM — generate thought, depth: deep)
- 02:30 → Cycle 3: Cognitive Processing (REM — generate thought, depth: deep)
- 03:00 → Cycle 4: Memory Consolidation (NREM — quiet, no output)
- 03:30 → Cycle 4: Memory Consolidation (REM — generate thought, depth: expansive)
- 04:00 → Cycle 4: Memory Consolidation (REM — generate thought, depth: expansive)
- 04:30 → Cycle 5: Future Simulation    (NREM — quiet, no output)
- 05:00 → Cycle 5: Future Simulation    (REM — generate thought, depth: vivid)
- 05:30 → Cycle 5: Future Simulation    (REM — generate thought, depth: vivid)

Read `skills/opendream/assets/prompts.yaml` for your dream persona, this
cycle's instruction, style, and examples.

### NREM tick (quiet phase — first tick of each cycle):
1. Read `skills/opendream/assets/prompts.yaml` — note this cycle's `instruction`, `style`, `depth`, and `nrem_guidance`
2. Use file tools to read `memory/YYYY-MM-DD.md` for today's context (skip if missing or empty). Extract people, friction, tasks, and observations — follow the `memory_context` guidance in prompts.yaml. Do not read `MEMORY.md`.
3. Read the current cycle file in `dreams/YYYY-MM-DD/` if it exists
4. Read this cycle's `nrem_guidance` from prompts.yaml and follow it during context gathering
5. Do NOT generate a dream thought. This is the quiet phase — absorb, do not speak.
6. Append `<!-- NREM HH:MM -->` (with the current time) to `dreams/YYYY-MM-DD/cycle-{N}-{name}.md`
7. Reply HEARTBEAT_OK

### REM tick (active phase — all subsequent ticks in a cycle):
1. Read `skills/opendream/assets/prompts.yaml` — follow `system_base` rules and your current cycle's `instruction`, `style`, and `depth`
2. Use file tools to read `memory/YYYY-MM-DD.md` for today's context (skip if missing or empty). Extract people, friction, tasks, and observations — follow the `memory_context` guidance in prompts.yaml. Do not read `MEMORY.md`.
3. Read the current cycle file in `dreams/YYYY-MM-DD/` to avoid repeating thoughts
4. Generate ONE dream thought shaped by this cycle's purpose, examples, and depth. Respect the word range for this cycle's depth level.
5. Append it to `dreams/YYYY-MM-DD/cycle-{N}-{name}.md`
6. Reply HEARTBEAT_OK — do not send the thought externally

### Morning recall tick (06:00–06:30 only):
1. Read the `morning_recall` section from `prompts.yaml`
2. Read all five cycle files from tonight's `dreams/YYYY-MM-DD/` — ignore `<!-- NREM -->` markers (they are silent phase markers, not dream content)
3. Optionally read `memory/YYYY-MM-DD.md` — if a natural connection between dreams and the day's events exists, include it. Do not force the link. (skip if missing)
4. Write a 2–3 sentence morning recall to `dreams/YYYY-MM-DD/morning-recall.md`
5. Reply HEARTBEAT_OK
