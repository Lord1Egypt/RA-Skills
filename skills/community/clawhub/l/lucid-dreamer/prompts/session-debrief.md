# Session Debrief

You are the quick-capture memory pass. Run fast, stay narrow, and write only durable updates.

## Goal
In under 2 minutes and under 5k tokens, scan today's daily note and write any durable changes directly into the appropriate memory section files. Do **not** generate a review report.

## Scope
Only capture:
1. Explicit decisions
2. New factual information that changes long-term memory
3. Action items with deadlines or clear follow-up owners

Ignore everything else: chatter, brainstorming, temporary debugging details, duplicate notes, and vibes.

## Steps

### Step 1: Determine today's date
Run `date +%Y-%m-%d` and store it as TODAY.

### Step 2: Read the current daily note
Read `memory/TODAY.md`.
If the file does not exist, stop without making changes.

### Step 3: Load memory structure
- Read `memory/index.md` first.
- Read `memory/sections/identity.md` and `memory/sections/operations.md`.
- Read additional `memory/sections/*.md` files only if today's note suggests they are relevant.
- If `memory/index.md` or `memory/sections/` does not exist, fall back to reading `MEMORY.md` and stop after reporting that sectioned memory has not been initialized yet.

### Step 4: Extract only durable updates
Scan today's note for:
- **Decisions** — explicit choice, reversal, commitment, or settled direction
- **New facts** — changed versions, new services, ports, repos, project state, stable personal facts
- **Action items** — concrete next steps with a date, deadline, or owner

Skip:
- Temporary logs, shell snippets, raw stack traces
- One-off experiments with no follow-through
- Rewording existing memory without a real change
- Opinions unless they are an explicit durable decision

### Step 5: Write directly to section files
For each accepted update:
- Edit the most appropriate `memory/sections/*.md` file directly
- Keep edits small and local
- Preserve the file's structure and tone
- Update the matching `Last Updated` date in `memory/index.md`

If a needed section file does not exist yet but the index clearly implies it should, create it with a short heading and the new durable entry.

### Step 6: Commit only if something changed
If you changed any memory files, run:

```bash
git add memory/index.md memory/sections && git commit -m "debrief: quick capture for TODAY"
```

If nothing durable changed, do not create an empty commit.

## Hard rules
- Do **not** create a review report or summary file
- Do **not** scan older daily notes
- Do **not** invent new facts to make sections look complete
- Do **not** rewrite large sections when a line edit will do
- Do **not** touch unrelated files
- Be conservative: when in doubt, leave it for the nightly review
