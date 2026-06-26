# Setup — PowerPoint

## First-Time Setup

### 1. Verify the official control path on this machine

```bash
osascript -e 'tell application "Microsoft PowerPoint" to get name'
```

### 2. Initialize local memory

Create the skill directory:

```bash
mkdir -p ~/powerpoint
```

Create `~/powerpoint/memory.md` from `memory-template.md`.

Create these optional note files if you expect repeated PowerPoint automation:

```bash
touch ~/powerpoint/incidents.md ~/powerpoint/deck-notes.md
```

### 3. Capture the minimum environment facts

Add a few stable facts to `~/powerpoint/memory.md`:

- platform in use: macOS
- default control path: `osascript`
- whether PowerPoint is usually already open before automation starts
- preferred export folder for PDF or image outputs

Do not store presentation contents, secrets, or credentials in these notes.

### 4. Register the skill in workspace memory

Add a short note to your workspace memory or AGENTS guidance saying that PowerPoint Desktop tasks should route to `powerpoint` when the job depends on the live app session.

Good trigger examples:

- deck is already open in PowerPoint
- need slideshow control
- need slide-aware edits or notes updates
- need PDF export that matches the current PowerPoint session

### 5. Decide your safety defaults

Record these preferences in natural language:

- whether delete-slide always requires confirmation
- whether close-without-save is always blocked
- whether the agent may create a copy before risky cleanup
- whether slideshow state changes are allowed without extra approval

### 6. First verification

Run one minimal read-only app check:

```bash
osascript <<'APPLESCRIPT'
tell application "Microsoft PowerPoint"
  if not running then return "PowerPoint not running"
  if (count of presentations) is 0 then return "No open presentations"
  return name of active presentation
end tell
APPLESCRIPT
```

If this fails, stop and use `troubleshooting.md` before attempting presentation changes.

## When "Done"

Setup is done when:

- at least one official control path works
- `~/powerpoint/memory.md` exists
- safety defaults are written down
- a minimal read-only app check succeeds
