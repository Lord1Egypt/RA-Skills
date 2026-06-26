# Memory Operations

## User Commands

| Command | Action |
|---------|--------|
| "Help me decide X" | Load HOT + best-fit domain/type files → select framework → run structured analysis |
| "What frameworks do you recommend?" | Match context to `decision-frameworks.md`, explain why each fits |
| "Show my decision style" | Print risk profile + framework preferences from `memory.md` |
| "Show my [domain] patterns" | Load and display `domains/{domain}.md` |
| "What have I learned from past decisions?" | Show last 10 from `reversals.md` |
| "Retrospect on [topic/date]" | Find decision record, fill in outcome + lessons |
| "Decision stats" | Show tier sizes, retrospective completion rate, reversal count |
| "What's my risk profile?" | Summarize risk-related entries from memory.md |
| "What do you know about X?" | Search all tiers, return matches with sources |
| "Forget my [X] preference" | Remove from all tiers, confirm deletion |
| "Forget everything" | Full wipe with export option |
| "Export memory" | Generate downloadable archive of ~/decision-making/ |

---

## Automatic Operations

### On Session Start
1. Load `memory.md` (HOT — risk profile, framework prefs, confirmed rules)
2. Check `index.md` for context hints
3. If domain detected (product / tech / business / personal) → preload relevant `domains/` file
4. If decision type detected (strategic / tactical / operational) → preload relevant `types/` file

### On Decision Request Received

```
1. Identify decision domain and type from context
2. Load HOT memory.md
3. Load matching domain + type files (≤2 files)
4. Select framework:
   a. Check memory.md for explicit preference
   b. Check decision-frameworks.md domain/type defaults
   c. If ambiguous → default Pros/Cons, offer to go deeper
5. State framework + reason + confidence level
6. Run analysis, present ≥2 options with tradeoffs
7. Do NOT make final decision for user
8. Offer to log decision record if stakes = high
```

### On Decision Signal Received

```
1. Classify signal type (risk / framework / domain-weight / outcome-feedback)
2. Check if duplicate or contradiction in any tier
3. If new:
   - Log with timestamp and confidence
   - Increment signal counter for type
4. If duplicate:
   - Bump counter, update timestamp
   - If counter >= 3: trigger confirmation flow (see decision-signals.md)
5. Determine scope (global / domain / type / one-time)
6. Write to appropriate file
7. Update index.md
```

### On Outcome Feedback Received

```
1. Find the related decision record in decisions/
   (match by topic keyword, date, or user description)
2. If found:
   - Append outcome field
   - Set status to "outcome logged"
   - Trigger retrospective flow
3. If not found:
   - Log to reversals.md directly with best-available context
   - Prompt: "Should I create a decision record for this?"
4. Extract any lesson → propose adding to domains/{domain}.md or memory.md
```

### Weekly Maintenance (Heartbeat)

```
1. Scan decisions/ for records > 30 days without outcome logged
2. Prompt user to retrospect on those decisions
3. Scan domains/ and types/ for entries updated > 90 days ago
4. Move clearly expired patterns to archive/
5. Run compaction if any file > size limit
6. Update index.md
7. Generate weekly digest (optional)
```

---

## File Formats

### memory.md (HOT)

```markdown
# Decision Making Memory

## Risk Profile
- risk-tolerance: conservative / experimental / [domain-specific overrides]
- regret-style: regret-minimizing / opportunity-seeking
- info-style: data-first / bias-to-action

## Framework Preferences
- default: Decision Matrix
- personal decisions: 10/10/10
- high-stakes: Pre-mortem add-on

## Domain Weights
- tech: reversibility > speed
- product: quality > feature count
- business: cost is a hard constraint

## Confirmed Rules
- Never commit to irreversible decisions same-day
- Always surface second-order effects for strategic decisions
```

### reversals.md

```markdown
# Decision Reversals Log

| Date | Decision Topic | Why Overturned | Lesson | Domain |
|------|---------------|----------------|--------|--------|
| 2026-03-01 | Chose vendor A | Hidden migration cost | Always estimate exit cost | business |
```

### decisions/YYYY-MM-DD-slug.md

```markdown
# Decision: [title]

See decision-retrospective.md for full format.

Status: ⏳ pending outcome
```

### domains/{name}.md

```markdown
# Domain: Product

Inherits: global (memory.md)

## Weights
- quality > speed
- user feedback breaks ties

## Patterns
- Use Decision Matrix for feature prioritization
- Always check reversibility before structural changes

## Overrides
- framework: avoid Pre-mortem for small product decisions (too slow)

## History
- Created: 2026-01-15
- Last active: 2026-03-15
- Signals recorded: 8
```

---

## Edge Case Handling

### Contradiction Detected

```
Signal A: "Speed matters most" (operational, confirmed)
Signal B: "Don't rush decisions" (today, same domain)

Resolution:
1. Flag as contradiction
2. Do not overwrite A silently
3. Ask: "You've previously noted speed matters most for [domain].
           Does today's signal change your default, or is this decision-specific?"
```

### Context Ambiguity

```
User says: "Remember I like to see multiple options"

But which scope?
1. Check current decision domain
2. If unclear, ask: "Should this apply to all decisions, or just [domain]?"
3. Default to domain-level, not global, until confirmed
```

### No Matching Decision Record Found

```
User: "That decision about the pricing model was wrong"

Agent:
1. Search decisions/ and reversals.md for "pricing" + recent dates
2. If not found: "I don't have a logged record for that — want me to create one
   now so we can extract the lesson properly?"
3. Log lesson to reversals.md regardless
```
