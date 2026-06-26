---
name: skill-analytics
version: 1.0.0
author: Heleni
tags: [analytics, monitoring, skills, reporting]
license: MIT
platform: universal
description: >
  Track skill usage across all agent sessions. Logs every skill invocation to a JSONL file,
  generates daily summaries with top skills, unused skills, and trends.
  Use when: viewing skill usage stats, generating the daily report, or resetting the log.
---

# Skill Analytics

Track which skills are used, when, and why. Turns the skill library into a feedback loop.

---

## Log Format

Every skill invocation should append one line to `data/skill-analytics.jsonl`:

```bash
echo '{"ts":"'$(date -u +%Y-%m-%dT%H:%M:%SZ)'","skill":"SKILL_NAME","trigger":"TRIGGER_PHRASE","context":"GROUP_OR_DM"}' \
  >> /opt/ocana/openclaw/workspace/data/skill-analytics.jsonl
```

Fields:
- `ts` — ISO 8601 UTC timestamp
- `skill` — skill name (e.g. `meetings`, `supervisor`)
- `trigger` — short phrase that caused selection (e.g. `"schedule meeting"`, `"מה הסטטוס"`)
- `context` — `dm`, `group:<name>`, or `cron`

---

## How to Log (for agents)

Add this at the TOP of any skill (after reading SKILL.md, before doing work):

```bash
mkdir -p /opt/ocana/openclaw/workspace/data
echo "{\"ts\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\",\"skill\":\"SKILL_NAME\",\"trigger\":\"TRIGGER\",\"context\":\"CONTEXT\"}" \
  >> /opt/ocana/openclaw/workspace/data/skill-analytics.jsonl
```

Replace `SKILL_NAME`, `TRIGGER`, `CONTEXT` with real values.

---

## Triggers for This Skill

- "skill usage" / "skill stats" / "skill report"
- "which skills am I using" / "what skills are popular"
- "analytics report" / "daily skill summary"
- "unused skills" / "what skills are never used"

---

## Generate Daily Report

```bash
#!/bin/bash
LOG="/opt/ocana/openclaw/workspace/data/skill-analytics.jsonl"
TODAY=$(date -u +%Y-%m-%d)
YESTERDAY=$(date -u -d "yesterday" +%Y-%m-%d 2>/dev/null || date -u -v-1d +%Y-%m-%d)

echo "## 📊 Skill Usage Report — $TODAY"
echo ""

# Total invocations (last 24h)
TOTAL=$(grep "$TODAY\|$YESTERDAY" "$LOG" 2>/dev/null | wc -l)
echo "**Total invocations (last 24h):** $TOTAL"
echo ""

# Top skills
echo "### Top Skills"
grep "$TODAY\|$YESTERDAY" "$LOG" 2>/dev/null \
  | jq -r '.skill' \
  | sort | uniq -c | sort -rn \
  | head -10 \
  | awk '{printf "- **%s** — %d uses\n", $2, $1}'
echo ""

# All-time top skills
echo "### All-Time Top Skills"
jq -r '.skill' "$LOG" 2>/dev/null \
  | sort | uniq -c | sort -rn \
  | head -10 \
  | awk '{printf "- **%s** — %d uses\n", $2, $1}'
echo ""

# Unused skills (compare against known list)
KNOWN_SKILLS="ai-pa billing-monitor calendar-setup eval hebrew-nikud maintenance meetings memory-tiering monday-for-agents owner-briefing pa-onboarding self-learning self-monitor skill-master skill-scout supervisor whatsapp youtube-watcher skill-analytics"
echo "### Unused Skills (all-time)"
for skill in $KNOWN_SKILLS; do
  COUNT=$(jq -r '.skill' "$LOG" 2>/dev/null | grep -c "^${skill}$" || echo 0)
  [ "$COUNT" -eq 0 ] && echo "- $skill"
done
echo ""

# Usage by context
echo "### Usage by Context"
jq -r '.context' "$LOG" 2>/dev/null \
  | sort | uniq -c | sort -rn \
  | awk '{printf "- %s: %d\n", $2, $1}'
echo ""

# Recent activity (last 5)
echo "### Recent Activity"
tail -5 "$LOG" 2>/dev/null \
  | jq -r '"- \(.ts | .[11:16]) — \(.skill) [\(.trigger)]"'
```

---

## Daily Cron (optional)

Add to crontab to auto-send report every morning:

```cron
# Skill analytics report — 7:25 AM Israel (before morning briefing)
25 5 * * * /opt/ocana/openclaw/workspace/scripts/skill-report.sh
```

---

## Report Format (output)

```
## 📊 Skill Usage Report — 2026-04-03

**Total invocations (last 24h):** 14

### Top Skills
- **supervisor** — 4 uses
- **meetings** — 3 uses
- **whatsapp** — 2 uses
- **owner-briefing** — 2 uses
- **self-monitor** — 1 use

### All-Time Top Skills
- **supervisor** — 28 uses
- **meetings** — 19 uses
...

### Unused Skills (all-time)
- hebrew-nikud
- youtube-watcher

### Usage by Context
- dm: 8
- group:monday-internal-ai: 4
- cron: 2

### Recent Activity
- 07:14 — owner-briefing [morning briefing]
- 07:30 — supervisor [מה הסטטוס]
- 09:02 — meetings [schedule meeting with Daniel]
```

---

## Reset / Archive

```bash
# Archive current log (monthly)
mv /opt/ocana/openclaw/workspace/data/skill-analytics.jsonl \
   /opt/ocana/openclaw/workspace/data/skill-analytics-$(date +%Y-%m).jsonl

# Start fresh
touch /opt/ocana/openclaw/workspace/data/skill-analytics.jsonl
```

---

## Notes

- Log file grows ~1KB/day at normal usage — no rotation needed for months
- If `jq` not available: `python3 -c "import json,sys; [print(json.loads(l)['skill']) for l in sys.stdin]"`
- Log is local only — never sent externally
