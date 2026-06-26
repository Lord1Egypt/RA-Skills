# Decision Retrospective

Track retrospectives for completed decisions. Each entry captures what the agent and user learned from evaluating a past decision against real-world outcomes.

---

## Format

```markdown
## [Date] — [Decision Slug]

**Decision:** What was actually decided
**When made:** Date of original decision
**Domain:** product / tech / business / personal
**Type:** strategic / tactical / operational
**Stakes:** low / medium / high
**Framework used:** What analysis was applied at the time
**Assumptions made:** Key assumptions that underpinned the decision

**Outcome:** What actually happened
**Expected outcome:** What was predicted
**Match:** ✅ as expected / ⚠️ partial / ❌ different / ⏳ too early to tell

**Quality assessment:**
- Process: sound / flawed / unclear
- Information used: complete / partial / insufficient
- Cognitive biases detected: none / [list specific biases]

**Lesson:** What to do differently next time
**Pattern update:** Was memory.md updated? (yes / no / pending)

**Status:** ⏳ pending outcome | 📋 outcome logged | ✅ lessons extracted | 📦 archived
```

---

## Example Entry

```markdown
## 2026-03-15 — adopt-nextjs-for-product

**Decision:** Migrate frontend stack from CRA to Next.js
**When made:** 2026-02-01
**Domain:** tech
**Type:** strategic
**Stakes:** high
**Framework used:** Decision Matrix (performance / DX / team familiarity / SEO)
**Assumptions made:** Team would adapt within 2 sprints; SEO improvement would be measurable in 60 days

**Outcome:** Migration took 4 sprints; SEO improved by 34% in 45 days
**Expected outcome:** 2 sprints; SEO impact visible within 60 days
**Match:** ⚠️ partial

**Quality assessment:**
- Process: sound — criteria were right, weights were reasonable
- Information used: partial — underestimated team's ramp-up time
- Cognitive biases detected: optimism bias on team velocity

**Lesson:** For tech migrations, add 2× buffer to team ramp-up estimates
**Pattern update:** yes — added to domains/tech.md: "migration timelines: 2× stated estimate"

**Status:** ✅ lessons extracted
```

---

## Cognitive Bias Reference

Use during quality assessment. Common biases in decision-making:

| Bias | Description | Detection Signal |
|------|-------------|-----------------|
| **Confirmation bias** | Seeking info that confirms existing preference | "I already knew this was the right call" |
| **Anchoring** | Over-weighting the first number / option seen | Estimate stayed close to initial figure |
| **Sunk cost** | Continuing because of past investment | "We've come too far to stop now" |
| **Optimism bias** | Underestimating difficulty / overestimating success | Timeline / cost was shorter than actual |
| **Availability heuristic** | Overweighting recent or vivid examples | "It worked for [recent case], so..." |
| **Status quo bias** | Preferring inaction or the default option | Chose the "safe" path without full analysis |
| **FOMO** | Deciding fast due to fear of missing out | Time pressure was artificial |
| **Overconfidence** | Confidence level higher than information warranted | 🟡 or 🔴 confidence felt like 🟢 |

---

## Retrospective Triggers

Log a retrospective when any of the following occurs:

1. User explicitly says the decision was right, wrong, or mixed
2. Heartbeat detects a decision record older than 30 days without an outcome
3. User revisits a past decision by name or date
4. Agent notices a contradiction between a past decision and new information

When triggering via heartbeat, prompt with:
```
"You made a decision about [topic] on [date] — have you seen results yet?
If so, a quick retrospective could sharpen future [domain] decisions."
```

---

## Promotion Rules

After a retrospective is completed:
- If **lesson** is applicable future pattern → add to `domains/{domain}.md` or `types/{type}.md`
- If **bias** appeared for the 2nd time → add bias awareness note to `memory.md`
- If **framework** was misapplied → update `decision-frameworks.md` domain default
- Decision record itself → stays in `decisions/` for 90 days, then moves to `archive/`

---

## Entries

(New retrospective entries are stored in `~/decision-making/decisions/YYYY-MM-DD-slug.md`)

This file is a **format reference only**. Individual decision records live in the `decisions/` directory.
