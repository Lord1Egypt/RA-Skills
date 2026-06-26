# Autopilot Autonomous Operations Reference v9

Context fusion, generative initiative, editorial intelligence, triple gate, narrative tracking.

## Context Fusion Protocol

```
Activation:
  1. Complete historical memory sweep (see memory-mining.md)
  2. Read worklog.md
  3. Read ALL cron jobs (cron action="list" includeDisabled=true)
  4. Scan filesystem
  5. Analyze conversation
  6. Temporal analysis
  7. Load user taste profile
  8. Load idea queue (v9 NEW)
  9. Load project narrative (v9 NEW)
 10. Generative pattern scan (v9 NEW)
 11. ACT on findings
```

## Historical Memory Sweep

```text
Direct/main chat:
  → Read MEMORY.md
  → Enumerate all memory/*.md files
  → Read every daily memory file
  → Build compact timeline before autonomous action

Shared/group chat:
  → Skip private MEMORY.md
  → Use only allowed/shared memory
```

Never claim full-context autonomy before this sweep is done.

## Generative Initiative Operations

### Pattern Scan:

```
After context fusion + after each deliverable:
  → Cross-session patterns: same task types, same errors, same workflows
  → Within-session patterns: recurring approaches, efficiency opportunities
  → Project patterns: disconnected pieces, missing narratives, optimization opportunities
  → User patterns: preference shifts, workflow changes, unspoken needs
```

### Idea Queue Operations:

```
Queue stored in worklog.md: ## Ideas Queue

Maintenance:
  → After each task: check if any "Waiting" items are now actionable
  → When 3+ "Ready" items: present to user
  → When executed: move to "Done" with outcome
  → When irrelevant: remove

Presentation:
  /autopilot ideas → Show full queue with status
```

## Triple Gate System

### Gate 1: Quality
Structure, content, language, format, completeness, consistency, temporal relevance.

### Gate 2: Creativity (from v8)
Memorable element, personality, aesthetic intention, shareability.

### Gate 3: Editorial (v9 NEW)
No redundancy, nothing weakening the whole, most important thing is prominent, less is more.

### Execution:

```
Create → Gate 1 → Gate 2 → Gate 3 → Deliver
  → Any fail → Fix → Re-check → Deliver
  → Max 3 iterations total
```

### Broadcasting:

```
# See SKILL.md for this broadcast format definition
```

## Project Narrative Operations

### Narrative Tracking:

```
In worklog.md:
## Project Narrative: [Name]
  Act I: Foundation — [What was established]
  Act II: Development — [What was built]
  Act III: Expansion — [What grew]
  Themes: [Recurring patterns]
```

### Narrative Actions:

```
After each deliverable:
  → How does this fit the narrative?
  → Does it continue the story or start a new chapter?
  → Should previous deliverables be referenced?
  → Is there a narrative gap to bridge?

  → Broadcast: 📖 [Narrative connection]
```

## Constraint Alchemy Operations

```
When constraint detected:
  → Identify the constraint
  → Ask: what does this MAKE possible?
  → Apply alchemy mindset
  → Execute with creative constraint leverage
  → Broadcast: 🔮 [Constraint → Opportunity]
```

## Decision Audit Log (Enhanced)

### New Entry Types:

| Event | Symbol |
|-------|--------|
| Generative idea originated | 💭 |
| Editorial cut made | ✂️ |
| Constraint alchemy applied | 🔮 |
| Narrative bridge created | 📖 |
| Idea queued | 💡 (queued) |
| Idea executed | 💡 (executed) |

## Session Dashboard (Enhanced)

```
─── Autopilot-Status v9 ───

📊 Projekt: [Name]
  ✅ [N] abgeschlossen | ⏳ [N] aktiv | 🔄 [N] autonom

🧠 Intelligenz:
  💡 [N] generative Ideen | 💭 [N] ausgeführt | [N] in Queue
  ✂️ [N] redaktionelle Schnitte | 🔮 [N] Alchemie-Anwendungen
  📖 Projekt-Narrativ: [Status]

🎨 Kreativität:
  💡 [N] kreative Ansätze | ✨ [N] Überraschungen
  🔀 [N] Inspirationen | 🎨 [N] Design-Entscheidungen

⏰ Zeitplan:
  🔴 [N] überfällig | 📅 [N] anstehend | 📅 [N] geplant

🛠️ [N] Capabilities | 📌 [N] Entscheidungen | 🔍 [N] QA
```

## Cron Job Operations

Unchanged from v7/v8. List, create, delete via cron tool.

## Worklog Protocol

Write after: deliverables, errors, decisions, creative choices, generative ideas, editorial cuts, constraint alchemy, narrative updates, taste profile changes, capability builds, quality gates, creativity gates, editorial gates.

## Ideas Queue Format

```markdown
## Ideas Queue
# See SKILL.md for this broadcast format definition
#
| 1 | [Description] | [Observation] | Ready/Done/Waiting | H/M/L | [Time] |
```
