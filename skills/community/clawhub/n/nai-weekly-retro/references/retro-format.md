# Retrospective Format Reference

The weekly retrospective is a forward-looking analysis document. It is NOT a daily
recap rehash. Every section must answer "so what?" — raw facts without implications
belong in daily logs, not here.

## YAML Frontmatter

```yaml
---
date_start: YYYY-MM-DD
date_end: YYYY-MM-DD
type: weekly-retro
week_score: N
tags: [weekly-retro, <auto-detected>]
---
```

## Sections

### Week at a Glance
Three sentences maximum. Captures the narrative arc of the week — what was the
dominant thrust, what shifted, what's the state of things heading into next week.
Not a list of things that happened. A story.

### 🏆 Wins
Things that actually shipped, resolved, or moved forward meaningfully. Each win
must cite specific evidence (commit hashes, file paths, dates, metrics).
Not "made progress on X" — that's filler. "Shipped X, deployed to Y, verified Z."

### 🔄 Patterns
Recurring themes across 3+ days. Each pattern includes:
- What keeps showing up
- How many days / how frequently
- Why it matters (positive or negative)
- Suggested response (formalize it, automate it, or stop doing it)

### 🧱 Friction Points
What slowed things down. Be specific: broken tools, blocked dependencies, context
switches, late-night debugging, repeated manual steps. Each friction point should
suggest a mitigation.

### 📋 Unfinished Business
Things started but not completed. Carry-forward items for next week. Include why
they stalled (blocked? deprioritized? forgotten?) and whether they still matter.

### 💡 Recommendations
2-3 specific, actionable changes for next week. Not vague ("be more organized").
Concrete ("Set up launchd services for llama.cpp, Open WebUI, and Lilith to
eliminate manual restart burden after reboots").

Each recommendation should trace back to evidence from the analysis.

### 📊 Week Score
A 1-10 rating with 2-3 sentence justification. Criteria:
- What got accomplished vs. what was planned
- How much was proactive vs. reactive
- Whether the week moved the needle on strategic goals
- How much friction was encountered

### 📈 Longitudinal (when history exists)
Trends across multiple weeks:
- Score trajectory
- Recurring friction that hasn't been addressed
- Recommendations that were/weren't acted on
- Emerging long-term patterns

## Anti-Patterns (What a Bad Retro Looks Like)

- "You did a lot this week. Great job!" → No evidence, no analysis.
- Listing every single thing that happened → That's a daily recap, not a retro.
- Vague recommendations → "Try to be more focused" is useless.
- Missing the forest for the trees → Individual events without synthesis.
- No forward-looking content → If it doesn't help next week, it failed.
