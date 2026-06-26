# Pattern Types — Detection Logic

The crystallizer detects four types of recurring patterns in memory logs.
Each type has different evidence requirements and suggestion outputs.

---

## 1. Recurring Request

**What it is:** The same category of ask appearing multiple times across different days.

**Detection signals:**
- High keyword overlap between events on different days
- Action verbs are similar (e.g., "researched", "analyzed" across multiple events)
- Entities may differ (different topics researched, but the act of researching recurs)

**Minimum evidence:** 3 occurrences across 2+ unique days

**Example:** "Ryan asked for market research" appearing on 3 separate days → suggest a research workflow template or monitoring cron.

**Output type:** Workflow shortcut or monitoring suggestion

---

## 2. Multi-Step Workflow

**What it is:** A sequence of 2+ steps that repeats in the same order.

**Detection signals:**
- Numbered steps, "then" chains, or arrow sequences (→) in the body text
- Sequential H3 subsections within H2 sections
- Action sequence matches (build → test → publish appearing multiple times)

**Minimum evidence:** 2 occurrences with strong step similarity, across 2+ days

**Example:** "Research gaps → build skills → test → publish to ClawHub → push to GitHub" appearing 3 times → suggest a dedicated skill that chains these steps.

**Output type:** Skill draft with the steps pre-defined

---

## 3. Time-Correlated Pattern

**What it is:** A request or workflow that happens at consistent times or on consistent days.

**Detection signals:**
- Time hints extracted from section headers (e.g., "2:00 AM ET")
- Same day-of-week appearing for 2+ events in a cluster
- Time-of-day clustering (morning, evening, etc.)

**Minimum evidence:** 2+ occurrences at similar times (±2 hours) or on the same day-of-week

**Example:** "Every Monday morning, Ryan asks for a project status update" → suggest a scheduled Monday briefing cron job.

**Output type:** Cron job definition with appropriate schedule

---

## 4. Event-Triggered Workflow (Reactive)

**What it is:** A consistent response to an external event type.

**Detection signals:**
- "When X happens, do Y" language patterns
- Sections triggered by external events (video drops, new releases, errors)
- Entity + action pairs that co-occur across events

**Minimum evidence:** 2+ occurrences with clear trigger-response structure

**Example:** "Whenever Ryan drops a YouTube video, summarize and vault it" → suggest formalizing as a standing workflow or reactive skill.

**Output type:** Varies — could be a skill, cron, or workflow shortcut

---

## What Does NOT Count as a Pattern

### Projects
Same entity with different actions over consecutive days. TokenPulse appearing 4 days in a row isn't a pattern — it's a project. Detected via high entity overlap + low action overlap.

### One-Day Bursts  
3+ similar events on the same day but never recurring. Building 18 skills in one sitting is a burst, not a recurring pattern. Filtered by requiring 2+ unique days.

### Already-Formalized Workflows
Patterns containing words like "cron job," "standing workflow," "pre-authorized," or "automated" are marked as already-formalized and deprioritized.

### Infrastructure Setup
One-time configuration tasks (installing software, setting up accounts). Distinguished by unique entities and setup-specific actions.

---

## Confidence Scoring

Each cluster gets a weighted confidence score:

| Factor | Weight | What it measures |
|--------|--------|-----------------|
| Occurrence count | 0.30 | More instances = stronger signal |
| Time span (days) | 0.25 | Spread across many days > same-day burst |
| Time correlation | 0.20 | Consistent timing suggests schedulability |
| Step consistency | 0.15 | Identical multi-step sequences = strong |
| Novelty | 0.10 | Not already automated = genuinely new |

**Threshold: 0.60** — clusters below this are logged but not surfaced as suggestions.

### Adjustments
- **< 7 days of data:** All suggestions marked "provisional"
- **> 14 days:** Thresholds can be slightly relaxed (more data = more confidence)
- **Rejected patterns:** Need 0.80+ confidence to re-surface
