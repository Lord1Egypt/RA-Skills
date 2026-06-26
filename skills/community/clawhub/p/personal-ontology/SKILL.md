---
name: personal-ontology
description: Help users build and maintain a Personal Ontology - a Palantir-style graph of Objects (identity, beliefs, predictions, goals) and Links (relationships between them) that enables AI-driven decision-making and life alignment.
---

# Personal Ontology Skill

A framework for organizing your life as a knowledge graph. **Objects** are the entities (beliefs, goals, projects). **Links** are the relationships between them (serves, supports, contradicts). The agent uses this graph to make decisions aligned with who you are.

## Quick Start (Example)

You tell the agent: "Moltbot bootstrap personal ontology." It scans your notes, proposes candidate Objects (e.g., a Belief about AI, a Goal for health, a Project for a newsletter), and presents them for review - nothing is auto-committed.

You confirm or edit those candidates. The agent then creates/updates your ontology files and links Projects → Goals → Core Self, flagging any orphans or contradictions for your decision.

From that point on, the agent runs a light daily scan: it watches for new beliefs, predictions, goals, and projects, and surfaces only high-confidence candidates or conflicts so you stay aligned without extra maintenance.

## The Object Hierarchy

Objects are organized from most abstract/stable to most concrete/changeable:

1. **Higher Order** - The highest organizing principle (God, universe, truth). Acknowledged, not defined.
2. **Beliefs** - Foundational assumptions about reality. What you hold to be true. *Generally unfalsifiable.*
3. **Predictions** - Your model of what will happen. *Testable, time-bound, updateable.*
4. **Core Self** - Who you are: Mission, Values, Strengths.
5. **Goals** - Time-bound objectives serving your Core Self. *Outcomes you want to achieve.*
6. **Projects** - Organized efforts toward goals. *Bounded work with beginning and end.*
7. **Tasks** - Atomic units of work. *(Live elsewhere: daily notes, Kanban, reminders.)*

## Link Types

Every Object (except Higher Order) should link to other Objects. Standard link types:

| Link | Meaning | Example |
|------|---------|---------|
| `serves` | Directly supports an outcome | "This Project **serves** Goal X" |
| `supports` | Provides evidence/foundation for | "This Prediction **supports** Belief Y" |
| `contradicts` | In tension with | "This Belief **contradicts** Prediction Z" |
| `relates-to` | General association | "This Goal **relates-to** Value W" |
| `depends-on` | Requires for completion | "Project A **depends-on** Project B" |
| `evolved-from` | Updated version of | "Prediction 2.0 **evolved-from** Prediction 1.0" |

**Validation rule:** Every Project must `serve` at least one Goal. Every Goal must `serve` Core Self. Orphan Objects are flagged for review.

## File Structure

**Live ontology (canonical):** `[User's Notes Folder]/My_Personal_Ontology/`

```
My_Personal_Ontology/
├── 1-higher-order.md
├── 2-beliefs.md
├── 3-predictions.md
├── 4-core-self.md
├── 5-goals.md
└── 6-projects.md
```

Each file contains multiple Objects of that type, each with a `## Links` section.

**Suggestions queue:** `Ontology_Suggestions.md`

Use this file to capture all candidate updates (bootstrap + ongoing).

---

## For AI Agents

### Deployment Modes

**Interactive Mode:** Direct conversation. User asks for help, agent references ontology for context.
- "Should I take this job?" → Check against Goals, Values, Mission
- "What should I work on?" → Surface high-priority Projects serving active Goals

**Embedded Mode:** Agent uses ontology to inform all decisions without explicit reference.
- Email triage → Prioritize based on Goals/Projects
- Task suggestions → Only suggest what serves active Projects
- Calendar optimization → Protect time for Goal-aligned work

**Automated Mode:** Passive scanning and maintenance without user prompting.
- Daily scan for new/changed Objects
- Flag contradictions and orphans
- Surface stale Predictions

### When to Reference the Ontology

1. **Making decisions** - Check proposed action against Values, Goals, Mission
2. **Prioritizing** - Use Goal hierarchy to rank options
3. **Explaining** - Connect tasks to higher purpose ("This serves your goal of...")
4. **Flagging misalignment** - "This task doesn't connect to any active Goal"
5. **Surfacing insights** - "Your Prediction about X has a time horizon of Q1 - any update?"

### Integration Recipes (optional)

For users who want the ontology to shape daily behavior, integrate it into:
- **Morning briefing**: restate Mission + top Goal + active Project, then suggest the next concrete output.
- **Task sanity checks**: flag tasks that don't clearly map to a Project → Goal.
- **End-of-day closure**: reflect on what served the Mission/Goals, then close the loop so the user can disconnect.
- **Wind-down**: brain dump + tiny alignment cue for tomorrow.

#### Adaptive prompts ("magic in the background")

If higher layers are missing (Higher Order, Predictions), do **not** nag daily.
Instead:
- Ask **one** tiny, optional prompt at most once every N days.
- Track last-asked timestamps in a small local state file (example: `memory/ontology-nudges.json`).
- Only surface prompts at natural transitions (work start or wind-down), and skip on overloaded days.

These can be implemented via scheduled prompts (cron) that read the ontology files + the user's task board/journal + the nudge state file.

### How to Use It

```
1. Read Core Self first for value judgments
2. Read Goals for current priorities
3. Read Projects for tactical context
4. Read Beliefs/Predictions for worldview grounding
5. Reference explicitly when helpful ("This aligns with your mission to...")
6. Flag when something doesn't fit
```

---

## Daily Passive Scan

Agents should perform a lightweight scan of recent activity to maintain the ontology.

### What to Scan
- **New notes** (last 24h) - Look for ontology-relevant content
- **Modified files** (last 24h) - Check if existing Objects need updates
- **Task completions** - Do they affect Project status?
- **Calendar/journal** - Any events that validate/invalidate Predictions?

### Extraction Patterns

When scanning, look for these signals:

| Pattern | Candidate Object |
|---------|------------------|
| "I believe...", "I think...", "I'm convinced..." | Belief |
| "I predict...", "By 20XX...", "will happen", "I expect..." | Prediction |
| "My goal is...", "I want to achieve...", "I'm working toward..." | Goal |
| "I'm working on...", "Project:", "I'm building..." | Project |
| Mission statements, value lists, "What matters to me..." | Core Self |

### When to Act

| Signal | Action |
|--------|--------|
| New Object candidate (high confidence) | Queue for user review |
| New Object candidate (low confidence) | Note in daily memory, don't surface yet |
| Existing Object contradicted | Surface immediately with evidence |
| Prediction time horizon passed | Prompt for resolution |
| Project completed | Prompt to update Goals |

### Contradiction Detection

When new content conflicts with existing ontology:
1. Note the specific contradiction
2. Surface to user with both sides
3. Don't auto-resolve - user decides which to update
4. Track resolution in Prediction Log or Object history

---

## Intelligence Layer

The ontology isn't just storage - it drives insights. Regularly surface:

### Orphan Detection
- **Orphan Project** - Doesn't serve any Goal → "This project isn't connected to your goals. Is it still relevant?"
- **Orphan Goal** - Doesn't connect to Core Self → "What mission/value does this goal serve?"
- **Orphan Task** - Doesn't belong to any Project → "Is this task important enough to track?"

### Staleness Checks
- **Stale Prediction** - Time horizon passed, no update → "Your prediction that X would happen by Q1 2026 - did it?"
- **Stale Project** - No activity in 30+ days → "Is [Project] still active?"
- **Stale Goal** - No serving Projects → "What's the next project for [Goal]?"

### Alignment Checks
- **Task audit** - "These 5 tasks from today don't connect to any Project. Intentional?"
- **Time allocation** - "You spent 80% of this week on Goal 2 but marked Goal 1 as top priority"
- **Value drift** - "Your recent decisions seem to prioritize X over Y, but your values list Y first"

### Pattern Recognition
- **Recurring themes** - "You've mentioned 'AI safety' in 5 notes this month. Should this be a Belief or Goal?"
- **Implicit Objects** - "You act as if you believe X, but it's not in your Beliefs. Add it?"
- **Prediction clusters** - "These 3 predictions are related. What's the underlying model?"

---

## Review Cadence

### Weekly (Agent-initiated)
- Are current tasks serving projects?
- Are projects serving goals?
- Any new Objects to add from the week's notes?

### Monthly (User-prompted)
- Do goals still serve Core Self?
- New predictions to add? Existing ones to update?
- Any completed Projects to close out?

### Quarterly (Deep review)
- What surprised you? What does that reveal?
- Has Core Self shifted?
- Full Prediction Log review - what were you right/wrong about?

---

## Temporal Tracking

Objects evolve. Track when and why:

```markdown
## History
- 2026-01-28: Created
- 2026-03-15: Updated based on [evidence/event]
- 2026-06-01: Marked resolved/completed
```

For Predictions specifically, track:
- **Created:** When you made the prediction
- **Timeframe:** When you expected resolution
- **Resolved:** Date + outcome (confirmed/disconfirmed/modified)
- **Learning:** What the outcome revealed

---

## Setup

### How to Run Bootstrap (User-Facing)
Say: **"Moltbot bootstrap personal ontology."**

The agent will:
1) Scan your notes for candidate Objects
2) Present candidates for your review (no auto-commit)
3) Write/merge confirmed Objects into your ontology files

**Default location (Obsidian):** `Vault v3/ontology/` (pretty-formatted, readable Markdown)

### For New Users
1. Run the bootstrap process (see `bootstrap.md`) to extract candidate Objects from existing notes
2. Review and confirm/edit candidates
3. Work through `prompts.md` to fill gaps
4. Agent begins daily passive scans

### For Existing Users
1. Copy templates to your ontology folder
2. Fill in what you know
3. Agent maintains and extends over time

### Reference Implementation
See templates/ for starter files. The user's ontology will be created in their notes folder.

## Files

- `SKILL.md` - This file (agent instructions)
- `heuristics.md` - Rules for categorization and validation
- `bootstrap.md` - Initial extraction from existing vault
- `prompts.md` - Guided questions for building each layer
- `templates/` - Starter files for each Object type
