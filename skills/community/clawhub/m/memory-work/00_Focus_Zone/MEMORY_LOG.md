---
title: Memory System Log
type: runtime-log
purpose: Memory system state and session operations
version: 1.0
---

# Memory System Log

## About This File

The **Memory Log** tracks what changed in your memory system — which insights were captured, where they live, what the AI learned about you this week, and what carries forward to next week.

**Who writes this?**
- The **memory-review** skill during your weekend archive
- Also written during any session with memory changes, architecture updates, skill creation, or parameter tweaks

**When does AI read it?**
- On session startup, AI reads only the **most recent entry** (not full history)
- This tells the AI what context changed, what actions were planned, and what to prioritize

**What happens if I disagree with something?**
- During memory-review, you'll have a chance to approve, reject, or correct each proposed entry
- Rejected items get marked with ✗ and a note about why
- If something seems wrong later, tell the AI and we'll correct the next log entry

---

## Baseline Parameters (v1.0)

These are the system defaults. They can be adjusted based on what works for you.

| Parameter | Value | Meaning |
|-----------|-------|---------|
| **Surprise threshold** | loose (capture first, filter later) | AI errs toward capturing too much rather than missing patterns |
| **Decay cycle** | 4 weeks inactive | Memory entries that aren't referenced for a month drop one priority level |
| **Procedural memory threshold** | 2+ behavioral evidence | AI needs to see a behavior at least twice before marking it as a pattern |
| **Review style** | open-ended, conversational | Questions like "what was hard?" not "did you complete task X?" |
| **Memory write confirmation** | always explicit | You approve each Layer 2/3 write before it goes in; no silent writes |

---

## Entry Template

Copy this template each week (AI will pre-fill dates and counts):

```
## Wnn [Review/Session] (YYYY-MM-DD)

### Memory Operations This Week
- Layer 2 writes: [count] entries added
- Layer 3 writes: [count] entries added  
- Memory retrievals: [count] times (AI referenced your patterns)
- User corrections: [count] (you said "no, that's wrong")
- User rejected writes: [count] (you said "don't capture that")

### Review Findings
High-confidence patterns discovered:
1. [Finding 1 with evidence]
2. [Finding 2 with evidence]

Questions or uncertainties:
- [Unclear pattern or potential confusion]

### Iteration Actions for Next Week
- [ ] [Action item 1 — something to test, track, or decide]
- [ ] [Action item 2]

### Parameter Adjustments
- [Parameter name]: [old value] → [new value]
- [Or: "No changes, maintain baseline"]

### Session Notes (Optional)
Any blockers in the memory system itself? Confusion about Layer definitions? Notes here.

---
```

---

## Sample Entry (Week 1)

Here's what an actual entry might look like:

```
## W06 Review (2026-02-16)

### Memory Operations This Week
- Layer 2 writes: 3 entries added
- Layer 3 writes: 2 entries added
- Memory retrievals: 7 times
- User corrections: 0
- User rejected writes: 0

### Review Findings
High-confidence patterns:
1. You prefer written material over meetings for decision-making (evidenced by 3 instances of pushing back on "let's sync live")
2. You iterate on visuals 3–4 times before shipping (spotted across presentation work, design docs, slides)
3. You batch-process blockers — don't mention them until they're actually stalling you

Questions:
- Do you want to capture the "visual iteration" as a working preference or as a potential inefficiency to address?

### Iteration Actions for Next Week
- [ ] Monitor whether week-end review time should shift from Sunday to Thursday (you've been archiving mid-week)
- [ ] Check if "async communication preference" is really a pattern or just this week's schedule

### Parameter Adjustments
- No changes, maintain baseline.

---
```

---

## How to Use This Log

### During Week
- You don't need to touch this file
- AI might read the last entry to understand context from last week

### At Weekend Review
- User runs memory-review skill
- AI proposes entries based on the week's work
- You approve, reject, or refine each proposal
- AI writes approved entries to this file

### Next Week
- AI reads the most recent entry on startup
- Uses "Iteration Actions" to follow up (e.g., "You wanted to test if visual iteration is a pattern — did that happen?")
- Uses updated parameters to adjust how it captures information

---

## Memory Layer Definitions (Quick Reference)

| Layer | Content | Lifespan | Graduation Path |
|-------|---------|----------|-----------------|
| **Layer 2** | Durable insights, preferences, patterns (how you think/work) | Multi-week | Becomes part of USER.md (stable personality traits) |
| **Layer 3** | Situation → action templates ("when X happens, you usually do Y") | As long as relevant | Stays in MEMORY.md until no longer applicable |

---

## Questions?

If you're unsure about something in the memory system, add a note here or tell the AI during memory-review. The system evolves with feedback.

---

**Latest Review**: [AI will timestamp the most recent entry]

**Next Review**: [AI will calculate based on calendar]
