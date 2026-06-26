# Dream Cycle Reference

Step-by-step procedure for running a dream cycle. This is an agent process —
not a script. You provide the judgment; the scripts handle the bookkeeping.

---

## What Is a Dream Cycle?

A dream cycle is a memory consolidation session. You review what happened
today, decide what's worth keeping long-term, update your memory accordingly,
and let the decay system prune what's no longer relevant.

The biological analogy is sleep-based memory consolidation: during REM sleep,
the hippocampus replays recent experiences and the neocortex integrates
significant ones into long-term storage. The dream cycle is that process,
made explicit and agent-orchestrated.

**It should not be automated.** The judgment of what matters cannot be
delegated to a script. A script can calculate scores and move tiers. Only you
can decide whether "interesting meeting with potential client" is worth keeping
or whether it's context that will never matter again.

---

## When to Run

**Nightly** is the default cadence. Run when the human is inactive — late at
night or before the first session of the morning. This mirrors the biological
model: consolidation happens during downtime.

**During heartbeats** also works. If you run periodic background checks, a
dream cycle can be included in the heartbeat procedure (every few heartbeats,
not every one).

**After a significant event:** job offer accepted, major decision made, new
system deployed, relationship context changed. Don't wait for the nightly cycle
if something important just happened.

**Skip it if:** nothing of significance happened today. A routine day with no
new facts, decisions, or context worth remembering doesn't warrant a dream cycle.
Write a single-line note to `dream-log.md` and move on.

---

## Full Procedure

### Step 0: Run memory-decay.js

Always start here. Recalculate decay scores before reviewing memory, so you're
working with current state.

```bash
node scripts/memory-decay.js
```

Check the output. Note:
- How many tier transitions occurred
- Any entries that were just archived (the script will tell you)
- Overall tier distribution

If any important entries just archived unexpectedly, check the archive file
(`memory/archive/YYYY-MM.md`) and decide whether to restore them.

---

### Step 1: Read today's daily note

Open `memory/YYYY-MM-DD.md` for today (and yesterday if yesterday's wasn't
processed). Read through everything.

As you read, mentally tag each item:
- **Keep** — significant, worth integrating into MEMORY.md
- **Skip** — routine, low-signal, or already in MEMORY.md
- **Supersede** — this item changes a fact already in MEMORY.md

Don't integrate yet. Finish reading first.

---

### Step 2: Integrate significant items

For each **Keep** item:

1. Find the right section in `MEMORY.md` (or create one if needed)
2. Add the bullet point
3. Keep it specific: facts, not impressions

For each **Supersede** item:

1. Identify the old entry in MEMORY.md
2. Update or replace the bullet
3. Run `memory-supersede.js` to update the temporal chain:

```bash
node scripts/memory-supersede.js \
  --old "<old fact text>" \
  --new "<new fact text>" \
  [--when "YYYY-MM-DD"]
```

Use `--when` if the change happened at a specific date that isn't today.

---

### Step 3: Prune stale entries

Review `MEMORY.md` with decay scores in mind. Run this to see what's low:

```bash
node -e "
  const d = JSON.parse(require('fs').readFileSync('memory/memory-meta.json','utf8'));
  const low = Object.values(d.entries)
    .filter(e => e.decayScore < 0.25 && !e.structural && e.tier === 'cold')
    .sort((a,b) => a.decayScore - b.decayScore)
    .slice(0, 20);
  low.forEach(e => console.log(e.decayScore.toFixed(3), e.tier, e.key));
"
```

For each low-score entry, ask: **does this still matter?**

- If no: remove the bullet from `MEMORY.md`. The meta entry will archive on
  the next decay run.
- If yes: do nothing. It'll be boosted when recalled.
- If uncertain: leave it. Low-cost to retain, costly to lose something you need.

**Be conservative.** The decay system will handle genuine forgetting over time.
Pruning is for entries you *know* are stale — old job negotiations, past server
configs you've migrated away from, outdated preferences.

---

### Step 4: Log to dream-log.md

Write a brief summary of the dream cycle to `memory/dream-log.md`:

```
[YYYY-MM-DD] Dream cycle.
  Reviewed: memory/YYYY-MM-DD.md
  Integrated: N items
  Pruned: N items
  Superseded: N entries
  Notable: <brief note on anything significant>
```

The dream-log.md is your audit trail. Over time it shows you how your memory
evolved — what you kept, what you dropped, when major facts changed.

The decay script also appends a line to dream-log.md automatically when it
runs. Your manual entry provides the context.

---

### Step 5 (optional): Re-run decay

If you added or removed many entries, run decay again to initialise scores for
the new entries and confirm the pruned ones are ready to archive.

```bash
node scripts/memory-decay.js --dry-run
```

New entries from bootstrap/integration start with `decayScore: 1.0`. That's fine.

---

## What to Integrate vs What to Skip

### Integrate if:

- It's a fact about the world that might be needed in a future session
  ("Project X: approved budget £50k", "Dev server migrated to new host")
- It's a preference or opinion that should shape future behaviour
  ("User prefers bullet lists over tables in Discord")
- It's a credential, connection detail, or configuration that isn't already
  captured ("New API key for service Y")
- It's a relationship fact ("Alice is now the new PM on Project Z")
- It changes context in a meaningful way
  ("Offer from Company X accepted — interviewing process closed")

### Skip if:

- It's a task completion with no lasting context
  ("Sent the invoice" — unless the invoice number matters long-term)
- It's a question the user asked once and you answered (no durable fact)
- It's already in MEMORY.md
- It's an observation about user mood or state (usually too transient)
- It's a draft or "might do" that didn't get decided
- It would clutter MEMORY.md without being useful in future sessions

**When unsure:** don't integrate. If it matters, it'll come up again. Let the
recall signal tell you whether it's worth keeping.

---

## How to Write Good Daily Notes

Daily notes are the raw material for dream cycles. Better notes → better
dream cycles → better long-term memory.

### Format

```markdown
# YYYY-MM-DD

## Sessions

### Session 1 — [brief context]

- [What happened, facts learned, decisions made]
- [New credentials or config encountered]
- [Context changes: project status, relationship updates]
- [Anything the agent might need to remember]

## Reminders for Tomorrow

- [Pending tasks]
- [Things to follow up on]
```

### What to capture:

- **Facts, not summaries.** "API key for Mailgun is xyz123" not "discussed API
  integration"
- **Decisions with context.** "Decided to use Postgres over MySQL because
  existing team expertise"
- **Changed state.** "Project Alpha: moved from proposal to signed contract"
- **New infrastructure.** IP addresses, port numbers, service names, credentials
- **People and roles.** "Alice joined as tech lead", "Bob left the project"

### What not to capture:

- Small talk, greetings, pleasantries
- Things already in MEMORY.md (unless they've changed)
- Internal agent reasoning (not durable facts)
- Emotional colour ("user seemed stressed") unless it's meaningful context

### Keep entries as bullet points

The dream cycle integration step picks up bullet-point entries. Headers and
prose are fine for structure, but the atoms of memory are bullets.

---

## Dream Log Format

`memory/dream-log.md` accumulates over time. The decay script writes:

```
[YYYY-MM-DD] [Memory Decay] Ran decay. Entries: N. Updated: N. Transitions: N. Archived: N. Tiers: {...}
```

Your manual entries follow this pattern:

```
[YYYY-MM-DD] Dream cycle.
  Reviewed: memory/2026-04-02.md
  Integrated: 3 items
  Pruned: 1 item (old project tracking entry)
  Superseded: 1 entry (project status updated)
  Notable: Big day. Offer accepted, old negotiations closed.

[YYYY-MM-DD] Dream cycle (skip — nothing to consolidate).
```

Keep entries brief. The log is for auditing, not storytelling.

---

## Example Dream Cycle Output

Here is a sample session showing the full cycle:

**Input:** `memory/2026-04-01.md` contains:

```markdown
# 2026-04-01

## Sessions

### Morning — Client update

- Got a call from Acme Corp at 10am — contract approved
- Terms: $120k/year, 20% bonus, 4 days remote
- Start date to confirm by April 7th
- Human is leaning heavily towards accepting

### Afternoon — Dev work

- Fixed CORS bug in the lead gen API (routes/api/v1/quotes)
- Updated nginx config on dev server to handle OPTIONS preflight
- nginx config: /etc/nginx/sites-enabled/app.conf
```

**Step 0:** Run decay. Output shows 2 entries just archived (old stale entries),
no significant transitions.

**Step 1:** Read the note. Tag:
- Acme Corp contract: **Keep** (significant decision context)
- nginx config path: **Keep** (structural — config path)
- CORS fix: **Skip** (task complete, low durable value)
- Human leaning towards accepting: **Skip** (mood/lean, not a decision)

**Step 2:** Integrate:

Add to MEMORY.md under `## Career`:
```
- Acme Corp: contract approved 2026-04-01. $120k/year, 20% bonus, 4d remote. Start date by April 7th.
```

Add to MEMORY.md under `## Infrastructure`:
```
- nginx config for app: /etc/nginx/sites-enabled/app.conf (dev server)
```

Run supersede for the old status:
```bash
node scripts/memory-supersede.js \
  --old "Acme Corp: proposal submitted" \
  --new "Acme Corp: contract approved. $120k, 20% bonus, 4d remote" \
  --when "2026-04-01"
```

**Step 3:** Prune. Check low-score entries. Find "Old staging server: 192.168.1.5"
with score 0.15 — that server was decommissioned months ago. Remove from MEMORY.md.

**Step 4:** Write to dream-log.md:
```
[2026-04-01] Dream cycle.
  Reviewed: memory/2026-04-01.md
  Integrated: 2 items (Acme Corp contract, nginx config path)
  Pruned: 1 item (old staging server IP)
  Superseded: 1 entry (Acme Corp status)
  Notable: Contract approved. Decision context now in MEMORY.md.
```

---

## Troubleshooting

**"The script archived an important entry."**
Check `memory/archive/YYYY-MM.md`. The entry's text is there. Re-add it to
`MEMORY.md` and re-run `memory-bootstrap.js` (it will skip existing entries
and add the re-introduced one). Consider whether it should be marked structural
— if so, adjust the patterns in `memory-bootstrap.js`.

**"memory-supersede.js can't find the old entry."**
The fuzzy matcher needs at least 25% word overlap. Try using more words from
the original bullet: `--old "Acme Corp: proposal submitted in March"`.
Or use `--dry-run` to see what the script finds before committing.

**"decayScore isn't changing."**
Run `memory-decay.js --verbose` to see individual entry calculations. Check that
`created` is set to a real date and not the far future (which would give `baseDecay > 1.0`).

**"MEMORY.md is getting too long."**
This is a real problem — very long MEMORY.md files slow context loading and
reduce signal-to-noise. Solutions:
1. Be more aggressive about pruning in dream cycles
2. Archive old sections (move them out of MEMORY.md into `memory/archive/`)
3. Split into domain-specific files and load selectively by session context
