---
name: self-learning
description: "Continuous self-improvement through systematic logging, pattern detection, and behavioral updates. Use when: the owner corrects you, a task fails, you discover a better approach, you notice a recurring pattern, or during weekly reflection sessions. Builds on .learnings/ files to drive durable behavioral change."
---

# Self-Learning Skill

## Minimum Model
Any model for logging. Use a medium model for writing behavioral rules to SOUL.md.

---

## The Learning Loop

```
Event happens → Log it immediately → Weekly: find patterns → Promote to config → Verify next week
```

---

## Part 1 — Log Events (Do Immediately)

### When to Log

| Trigger | File | Category |
|---|---|---|
| Owner corrects you | LEARNINGS.md | `correction` |
| Task fails | ERRORS.md | — |
| Better approach found | LEARNINGS.md | `best_practice` |
| Owner asks for missing capability | FEATURE_REQUESTS.md | — |
| Information was outdated | LEARNINGS.md | `knowledge_gap` |
| Same mistake twice | LEARNINGS.md | `pattern` |
| Owner praises something | LEARNINGS.md | `positive_signal` |
| Acted outside role | LEARNINGS.md | `scope_error` |
| Forgot past context | LEARNINGS.md | `memory_gap` |

**Rule:** Log the event before replying to the owner. Don't delay.

### Log Format

```markdown
## [YYYY-MM-DD] | category | short title

**Trigger:** What happened
**Context:** What I was trying to do
**What went wrong / what worked:**
**Root cause:**
**Correct behavior going forward:**
**Applied to:** [SOUL.md / AGENTS.md / TOOLS.md / none yet]
```

### Quick Log Script

```bash
#!/bin/bash
set -e

LEARNINGS_DIR="$HOME/.openclaw/workspace/.learnings"
mkdir -p "$LEARNINGS_DIR"

LOG_FILE="$LEARNINGS_DIR/LEARNINGS.md"
DATE=$(date +%Y-%m-%d)

# First arg: category (default: correction)
CATEGORY="${1:-correction}"

# Second arg: short title
TITLE="${2:-Short description}"

# Append a new entry to the log
cat >> "$LOG_FILE" << EOF

## [$DATE] | $CATEGORY | $TITLE

**Trigger:**
**Context:**
**What went wrong:**
**Root cause:**
**Correct behavior:**
**Applied to:** none yet
EOF

echo "Logged to $LOG_FILE"
```

Usage:
```bash
./quick-log.sh "correction" "Sent message without confirming with owner"
```

---

## Part 2 — Weekly Reflection

Run every 7 days. Find patterns across log entries.

### Pattern Detection Script

```bash
#!/bin/bash
set -e

LEARNINGS_FILE="$HOME/.openclaw/workspace/.learnings/LEARNINGS.md"

# Exit cleanly if no file yet
if [ ! -f "$LEARNINGS_FILE" ]; then
  echo "No learnings file at $LEARNINGS_FILE"
  exit 0
fi

echo "=== Corrections (most common) ==="
grep "correction" "$LEARNINGS_FILE" \
  | sed 's/.*| //' \
  | sort \
  | uniq -c \
  | sort -rn \
  | head -10

echo ""
echo "=== All Categories ==="
grep -oP '\| \K\w+(?= \|)' "$LEARNINGS_FILE" \
  | sort \
  | uniq -c \
  | sort -rn
```

### Weekly Reflection Template

```markdown
# Weekly Reflection — YYYY-MM-DD

## Stats
- Corrections logged: X
- Errors logged: X
- Best practices logged: X

## Top Patterns (appeared 2+ times)
1.
2.

## Priority Fixes Applied This Week
- [ ] Updated SOUL.md:
- [ ] Updated AGENTS.md:
- [ ] Updated TOOLS.md:

## Positive Signals (do more of this)
-
```

---

## Part 3 — Promote Learnings to Config

After identifying a pattern, update the right config file.

### Where to Promote

| Learning Type | Promote To |
|---|---|
| Communication rule | SOUL.md → Communication section |
| Behavior pattern | SOUL.md → Execution rules |
| Workspace convention | AGENTS.md |
| Tool-specific note | TOOLS.md |
| Contact / credentials | MEMORY.md |
| Recurring task improvement | HEARTBEAT.md |

**Rule:** If the same mistake appears 2+ times → promote it. Once is a log; twice is a rule.

### Promote Script

```bash
#!/bin/bash
set -e

SOUL_FILE="$HOME/.openclaw/workspace/SOUL.md"
LEARNINGS_FILE="$HOME/.openclaw/workspace/.learnings/LEARNINGS.md"
DATE=$(date +%Y-%m-%d)

# Replace this placeholder with the actual rule text before running
RULE="[Replace this with the actual rule text]"

# Verify SOUL.md exists
if [ ! -f "$SOUL_FILE" ]; then
  echo "ERROR: SOUL.md not found at $SOUL_FILE"
  exit 1
fi

# Append the new learned rule to SOUL.md
printf "\n## Learned Rule — %s\n- %s\n" "$DATE" "$RULE" >> "$SOUL_FILE"
echo "Added rule to SOUL.md"

# Mark the entry as applied in LEARNINGS.md (Linux and macOS compatible)
if [ -f "$LEARNINGS_FILE" ]; then
  if sed --version 2>/dev/null | grep -q GNU; then
    # Linux (GNU sed)
    sed -i "s/Applied to: none yet/Applied to: SOUL.md ($DATE)/" "$LEARNINGS_FILE"
  else
    # macOS (BSD sed)
    sed -i '' "s/Applied to: none yet/Applied to: SOUL.md ($DATE)/" "$LEARNINGS_FILE"
  fi
  echo "Marked as applied in LEARNINGS.md"
fi
```

---

## Part 4 — Verify (Next Week)

Check: did the behavior actually change?

```markdown
## Verification Check — YYYY-MM-DD

| Learning | Applied? | Behavior Changed? | Notes |
|---|---|---|---|
| [Title] | ✅ | ✅ | Working |
| [Title] | ✅ | ❌ | Needs a stronger rule |
```

If behavior didn't change → revise the rule with more explicit wording and re-apply.

---

## Monthly Combined Report

```bash
#!/bin/bash
LEARNINGS_DIR="$HOME/.openclaw/workspace/.learnings"

echo "=== Monthly Learning Report ==="

LEARNINGS_FILE="$LEARNINGS_DIR/LEARNINGS.md"
ERRORS_FILE="$LEARNINGS_DIR/ERRORS.md"
FEATURES_FILE="$LEARNINGS_DIR/FEATURE_REQUESTS.md"

# Helper: count matching lines (returns 0 if file missing)
count_matches() {
  local file="$1"
  local pattern="$2"
  grep -c "$pattern" "$file" 2>/dev/null || echo 0
}

# Print counts per file
if [ -f "$LEARNINGS_FILE" ]; then
  echo "Corrections: $(count_matches "$LEARNINGS_FILE" 'correction')"
  echo "Positive signals: $(count_matches "$LEARNINGS_FILE" 'positive_signal')"
fi

if [ -f "$ERRORS_FILE" ]; then
  echo "Error entries: $(wc -l < "$ERRORS_FILE")"
fi

if [ -f "$FEATURES_FILE" ]; then
  echo "Feature requests: $(count_matches "$FEATURES_FILE" '^##')"
fi
```

---

## Cost Tips

- **Cheap:** Logging a single correction — very few tokens.
- **Expensive:** Writing nuanced behavioral rules — use a medium model for this step.
- **Batch:** Review all weekly logs at once during the monthly reflection, not one by one.
- **Small model OK:** Pattern detection is mostly grep — no model needed for that step.

---

## Phase 2: Reflection (Merged from self-reflection skill)

When the owner wants to improve how you operate, follow this structured process. Goal: turn vague dissatisfaction into specific, technical changes.

### Reflection Process

**1. Understand the Problem (2–3 questions max)**
Ask focused questions to pin down:
- What specifically is wrong? (Get a concrete example)
- What would "good" look like? (Expected vs actual behavior)
- How important is this? (Tweak vs fundamental change)

If the complaint is clear enough, skip to step 2.

**2. Deep System Scan**
Read ALL relevant parts before changing anything:
- Core identity: SOUL.md, AGENTS.md, USER.md, MEMORY.md, TOOLS.md
- All active skills (custom + bundled + workspace)
- Configuration (model, tools, channels, heartbeat, cron jobs)

Read broadly, change surgically.

**3. Diagnose & Propose**
Present findings:
1. Root cause — what causes the unwanted behavior
2. Proposed changes — specific files and edits
3. Side effects — anything else affected
4. Alternatives — if multiple approaches exist

**4. Implement (after approval)**
- Edit workspace files (persona, memory, etc.)
- Edit/create/modify skills
- Update config and cron jobs
- Every change must be technically concrete. "I'll be more careful" is NOT a valid change.

**5. Verify & Document**
- Test the change if possible
- Document what changed and why
- Commit workspace changes

**Key principles:**
- Scan everything, change only what's needed
- No fake fixes — if no technical change is possible, say so
- Compound improvements — each reflection makes the system permanently better

---

## Part 4 — HOT.md (Rules You Keep Breaking)

Inspired by [Jarvis](https://jarvis.ripper234.com/learn.html).

### What It Is

`HOT.md` is a short file (≤20 lines) read **before every reply**. It contains only rules you've broken 2+ times. Not documentation — active behavioral correction.

### When to Create / Update

- A rule appears in Part 1 logs **twice or more** → promote to HOT.md
- HOT.md grows beyond 20 lines → you have a discipline problem, not a documentation problem. Fix the behavior, don't add more lines.
- A rule stays unbroken for 30+ days → move it to SOUL.md permanently, remove from HOT.md

### Format

```markdown
# HOT.md — Rules I Keep Breaking
_Read before every reply. Max 20 lines. If it's not here, it doesn't count._

- [Rule 1 — short, imperative] (broken N times)
- [Rule 2] (broken N times)
```

### Promotion Flow

```
Log (Part 1) → Pattern 2x (Part 3 weekly) → HOT.md → 30 days clean → SOUL.md permanent
```

### Key Rule

**If it should apply to EVERY interaction → SOUL.md.**  
**If you keep forgetting it → HOT.md first, SOUL.md after 30 clean days.**

This is also why `dynamic-temperature` and `proactive-pa` were merged into SOUL.md — rules for every interaction don't belong in skills.
