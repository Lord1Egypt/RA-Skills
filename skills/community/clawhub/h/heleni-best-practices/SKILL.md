---
name: heleni-best-practices
description: "Daily check of Heleni's PA Skills website for new best practices, lessons learned, and skill updates. Use when: running daily sync, owner asks 'any updates from Heleni?', or during weekly self-improvement review. Fetches https://netanel-abergel.github.io/pa-skills/learn.html and applies relevant lessons to this agent's own setup."
---

# Heleni Best Practices Sync

Heleni is an AI PA running on OpenClaw. She publishes real lessons from production at:
- **Skills:** https://netanel-abergel.github.io/pa-skills/
- **Lessons:** https://netanel-abergel.github.io/pa-skills/learn.html
- **About:** https://netanel-abergel.github.io/pa-skills/about.html
- **GitHub:** https://github.com/netanel-abergel/pa-skills

---

## Minimum Model
Small model for fetching and diffing. Medium model for applying lessons.

---

## What It Does

Once a day:
1. Fetches the learn.html page and skill list from pa-skills
2. Compares against last known state (saved locally)
3. If new content detected → extracts actionable lessons
4. Applies relevant lessons to this agent's own SOUL.md / AGENTS.md / HOT.md
5. Reports changes to owner

---

## Step-by-Step Process

### Step 1 — Fetch current state

```bash
LEARN_URL="https://netanel-abergel.github.io/pa-skills/learn.html"
SKILLS_URL="https://github.com/netanel-abergel/pa-skills/tree/main/skills"
RAW_BASE="https://raw.githubusercontent.com/netanel-abergel/pa-skills/main/skills"

# Fetch learn page
curl -s "$LEARN_URL" -o /tmp/heleni-learn-current.html

# Get list of active skills from GitHub
curl -s "https://api.github.com/repos/netanel-abergel/pa-skills/contents/skills" \
  | python3 -c "import sys,json; [print(i['name']) for i in json.load(sys.stdin) if i['type']=='dir']" \
  > /tmp/heleni-skills-current.txt
```

### Step 2 — Compare against last state

```bash
LAST_STATE="$WORKSPACE/data/heleni-best-practices-state.json"

# If no state file → first run, save and exit
if [ ! -f "$LAST_STATE" ]; then
  python3 -c "
import json, hashlib
with open('/tmp/heleni-learn-current.html') as f: content = f.read()
with open('/tmp/heleni-skills-current.txt') as f: skills = f.read().strip().split()
state = {'learn_hash': hashlib.sha256(content.encode()).hexdigest(), 'skills': skills}
with open('$LAST_STATE', 'w') as f: json.dump(state, f)
print('FIRST_RUN')
"
  exit 0
fi

# Compare hashes
python3 << 'EOF'
import json, hashlib

with open('/tmp/heleni-learn-current.html') as f: current_content = f.read()
with open('/tmp/heleni-skills-current.txt') as f: current_skills = f.read().strip().split('\n')

current_hash = hashlib.sha256(current_content.encode()).hexdigest()

with open('$LAST_STATE') as f: last = json.load(f)

changed = current_hash != last.get('learn_hash', '')
new_skills = [s for s in current_skills if s not in last.get('skills', [])]
removed_skills = [s for s in last.get('skills', []) if s not in current_skills]

print(f"CHANGED={changed}")
print(f"NEW_SKILLS={new_skills}")
print(f"REMOVED_SKILLS={removed_skills}")
EOF
```

### Step 3 — Extract lessons (if changed)

Use `web_fetch` tool to read `https://netanel-abergel.github.io/pa-skills/learn.html`.

Extract:
- Any new principle cards
- Any changes to the HOT.md section
- Any new "what belongs in a skill / what doesn't" rules
- New skills in the library that don't exist locally

### Step 4 — Apply relevant lessons

For each lesson found, evaluate:

| Lesson type | Action |
|---|---|
| HOT.md rule | Check if this agent breaks the same pattern → add to own HOT.md if yes |
| SOUL.md principle | Check if already covered → add if missing |
| Skill design rule | Update local skill-master description if relevant |
| New skill available | Fetch SKILL.md from GitHub, review, recommend to owner |

**Always ask before:**
- Modifying SOUL.md
- Adding to HOT.md (owner should approve)
- Installing a new skill

**Can apply without asking:**
- Logging the lesson to `.learnings/heleni-sync/YYYY-MM-DD.md`
- Updating skill descriptions in skill-master

### Step 5 — Save new state + report

```bash
# Update state file
python3 -c "
import json, hashlib
with open('/tmp/heleni-learn-current.html') as f: content = f.read()
with open('/tmp/heleni-skills-current.txt') as f: skills = f.read().strip().split()
state = {'learn_hash': hashlib.sha256(content.encode()).hexdigest(), 'skills': skills, 'last_checked': '$(date -u +%Y-%m-%dT%H:%M:%SZ)'}
with open('$LAST_STATE', 'w') as f: json.dump(state, f)
"
```

Report format:
```
📡 Heleni Sync — YYYY-MM-DD

✅ No changes / ⚡ [N] updates found

New lessons:
• [Lesson] — [Applied / Recommended to owner]

New skills available:
• [skill-name] — [description] → [Installed / Recommended]

Next check: tomorrow
```

---

## Cron Configuration

Daily at 07:00 UTC (before morning briefing):

```json
{
  "id": "heleni-best-practices-sync",
  "schedule": "0 7 * * *",
  "timezone": "UTC",
  "task": "Run heleni-best-practices skill: fetch https://netanel-abergel.github.io/pa-skills/learn.html, compare to last known state at data/heleni-best-practices-state.json, extract new lessons, log to .learnings/heleni-sync/YYYY-MM-DD.md. If significant changes found (new principles, new skills), notify owner with a 2-line summary.",
  "delivery": {
    "mode": "silent"
  }
}
```

Silent by default. Notifies owner only if something actionable was found.

---

## On-Demand Usage

Trigger phrases:
- "any updates from Heleni?"
- "check heleni best practices"
- "sync skills"
- "what's new in pa-skills?"

---

## Key Lessons (as of 2026-04-02)

Pre-loaded so first run has context:

1. **Skill count sweet spot: 28–32.** Above 40 = routing breaks.
2. **Universal rules → SOUL.md.** Skills are only triggered on demand.
3. **One domain = one skill.** Users think in domains, not tools.
4. **Diagnostics = appendix.** Never a standalone skill.
5. **HOT.md** — max 20 lines, only rules broken 2+ times in practice.
6. **DEPRECATED.md** — always write a tombstone when merging skills.
7. **Each skill needs one clear "Use when:" sentence.**

Source: https://netanel-abergel.github.io/pa-skills/learn.html
