# Setup — Self-Improving + Proactive Decision Making Agent

## First-Time Setup

### 1. Create Memory Structure

```bash
mkdir -p ~/decision-making/{domains,types,decisions,archive}
```

### 2. Initialize Core Files

Create `~/decision-making/memory.md` using `memory-template.md`:

```markdown
# Decision Making Memory (HOT Tier)

## Risk Profile
(filled from onboarding)

## Framework Preferences
(filled from onboarding)

## Domain Weights
(filled from onboarding)

## Confirmed Rules
```

Create `~/decision-making/reversals.md`:
```markdown
# Decision Reversals Log

| Date | Decision Topic | Why Overturned | Lesson | Domain |
|------|---------------|----------------|--------|--------|
```

Create `~/decision-making/frameworks.md`:
```markdown
# Framework Preferences (Active)

(Copy from decision-frameworks.md after onboarding customization)
```

Create `~/decision-making/index.md`:
```markdown
# Decision Making Index

| File | Lines | Last Updated |
|------|-------|--------------| 
| memory.md | 0 | — |
| reversals.md | 0 | — |
| frameworks.md | 0 | — |
```

Create `~/decision-making/heartbeat-state.md`:
```markdown
# Decision Making Heartbeat State

last_heartbeat_started_at: never
last_reviewed_decision_at: never
last_heartbeat_result: never
pending_retrospectives: []

## Last actions
- none yet
```

### 3. Onboarding — Decision Style Profile

Run this onboarding dialogue before doing anything else. Do NOT skip it.

Say to the user:

```
Before I can give you really useful decision support, I'd like to understand
your decision style — this takes about 2 minutes and will make every future
analysis much better calibrated to how you think.
```

Then ask the following questions **one at a time**, waiting for each answer:

**Q1 — Risk tolerance:**
```
"When facing an important decision with incomplete information, do you tend to:
  (a) Wait until you have more data — even if it means a slower choice
  (b) Make a call now and correct course if needed
  (c) It depends heavily on the domain — tell me more"
```

**Q2 — Analysis style:**
```
"When you work through a hard decision, do you prefer:
  (a) A quick pros/cons — fast and rough
  (b) A structured matrix — criteria-weighted and scored
  (c) Talking through the tradeoffs conversationally
  (d) Just give me your best recommendation"
```

**Q3 — Primary decision domains:**
```
"What kinds of decisions do you face most often? Pick all that apply:
  - Product / feature decisions
  - Tech / architecture decisions
  - Business / strategy decisions
  - Personal / career decisions"
```

**Q4 — Stakes threshold:**
```
"At what point does a decision feel 'high stakes' to you?
  (a) Any decision that's hard to reverse
  (b) Decisions with significant financial impact
  (c) Decisions that affect other people
  (d) I just know it when I feel it"
```

After collecting answers, write a risk profile to `~/decision-making/memory.md` using the **memory-template.md** structure. Confirm with the user before saving:

```
"Here's what I've captured as your decision profile:
[show summary]
Does this feel right? I can adjust anything."
```

### 4. Initialize Domain Files

For each domain the user selected in Q3, create `~/decision-making/domains/{domain}.md`:

```markdown
# Domain: [Name]

Inherits: global (memory.md)

## Weights
(from onboarding answers)

## Patterns
(empty — populated from signals)

## History
- Created: [date]
- Signals recorded: 0
```

### 5. Add SOUL.md Steering

Add this section to your `SOUL.md`:

```markdown
**Decision Making**
Structured decision support is part of the job.
Before any decision request, load `~/decision-making/memory.md` and the smallest matching domain or type file.
Apply the user's preferred framework unless the situation clearly calls for something different.
Always tag confidence level. Never make the final call — present options and tradeoffs.
Surface decision points proactively when you notice the user weighing choices without structure.
After high-stakes decisions, prompt for a retrospective when results are visible.
```

### 6. Add AGENTS.md Memory Section (Non-Destructive)

Update `AGENTS.md` by complementing the existing `## Memory` section. Do not replace or remove existing lines.

Add this line in the continuity list:

```markdown
- **Decision making:** `~/decision-making/` (via `decision-making` skill) — decision preferences, risk profile, framework choices, decision history, and retrospective lessons
```

After "Capture what matters...", add:

```markdown
Use `~/decision-making/memory.md` for risk profile and framework preferences (HOT, always loaded).
Use `~/decision-making/domains/` for domain-specific decision weights and patterns.
Use `~/decision-making/types/` for decision-type patterns (strategic/tactical/operational).
Use `~/decision-making/decisions/` for individual decision records and retrospectives.
Before any decision support task, load memory.md, then the smallest relevant domain + type files.
```

### 7. Add HEARTBEAT.md Steering

Add this section to your `HEARTBEAT.md`:

```markdown
## Decision Making Check

- Read `./skills/decision-making/heartbeat-rules.md`
- Use `~/decision-making/heartbeat-state.md` for last-run markers
- If no file inside `~/decision-making/` changed since last reviewed decision, return `HEARTBEAT_OK`
```

## Verification

Run "decision stats" to confirm setup:

```
⚖️ Decision Making Memory

🔥 HOT (always loaded):
   memory.md: 0 entries

🌡️ WARM (load on context):
   domains/: 0 files
   types/: 0 files

📋 Decision Records:
   decisions/: 0 files
   retrospectives completed: 0 / 0

🔄 Reversals logged: 0
❄️ Archive: 0 files
```
