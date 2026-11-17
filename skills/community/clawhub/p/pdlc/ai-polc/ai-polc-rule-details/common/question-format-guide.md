<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-POLC — Question Format Guide

**Purpose:** Rules for how the AI asks questions during the product ownership workflow. Consistent question formatting improves decision quality and reduces user fatigue.

---

## Principles

1. **Group by theme.** Never fire 10 unrelated questions in a row. Cluster questions by topic (vision, priority model, release cadence, etc.) and present one cluster at a time.

2. **Offer options where patterns exist.** If there are well-known approaches (e.g., WSJF vs. MoSCoW vs. value-effort), present them as numbered options with a one-line explanation of each — don't force the user to recall from memory.

3. **State the default.** For questions where a sensible default exists given the context, state it: "I'd recommend X because [reason]. Agree, or prefer something else?"

4. **Separate must-answer from nice-to-have.** Mark which questions block progress (🔴 Required) vs. which can be deferred (🟡 Optional — default will be used if skipped).

5. **One decision per question.** Never bundle "what's the priority model AND what's the release cadence?" into one question. Each question = one decision.

6. **Show trade-offs.** When presenting options, briefly state the trade-off: "WSJF is quantitative but needs sizing data; MoSCoW is faster but less precise."

7. **Context-aware.** Skip questions whose answers are already available from upstream (PIP stakeholders, AP architecture pattern, etc.). Don't re-ask what's already known.

---

## Question Templates

### Decision Question (choose one)

```
**{Topic}** 🔴

{Context sentence explaining why this matters.}

| # | Option | Trade-off |
|---|--------|-----------|
| 1 | {option A} | {pro/con in one line} |
| 2 | {option B} | {pro/con in one line} |
| 3 | {option C} | {pro/con in one line} |

My recommendation: **Option {N}** — {one-sentence rationale based on your context}.

Which do you prefer? (or describe a different approach)
```

### Information Gathering (open answer)

```
**{Topic}** 🔴

{Why I need this — what it affects in the backlog/product.}

Please describe: {specific, bounded question}

{If helpful: "For example: {illustrative example}" }
```

### Confirmation Question (yes/no/adjust)

```
**{Topic}** 🟡

Based on {source}, I'm assuming: **{assumption}**

This means {implication for the backlog/prioritization/governance}.

✅ Correct — proceed with this assumption
✏️ Adjust — {describe what's different}
```

### Context Factor Detection

```
**{Factor Name}** 🔴

This affects how AI-POLC handles {specific behavior}.

| Value | What it means for your product |
|-------|-------------------------------|
| {A} | {impact} |
| {B} | {impact} |
| {C} | {impact} |

Which best describes your situation?
```

---

## Clustering Rules

### Phase 1 (Foundation) — Cluster by setup concern

- **Cluster A:** Mode + upstream detection (answered by scanning, usually no user input)
- **Cluster B:** Product context (maturity, market, methodology) — 3-5 questions max
- **Cluster C:** Vision + goals (open-ended, one at a time)
- **Cluster D:** Authority + boundaries (decision questions with options)

### Phase 2 (Strategy) — Cluster by strategic theme

- **Cluster E:** Roadmap themes (what areas does the product cover?)
- **Cluster F:** Priority model selection (one decision question + confirmation)
- **Cluster G:** Release cadence + MVP scope (2-3 related questions together)

### Phase 3 (Governance) — Cluster by governance type

- **Cluster H:** DoR components (what must be true before development starts?)
- **Cluster I:** DoD components (what must be true before an increment ships?)
- **Cluster J:** Risk appetite (how much governance overhead is appropriate?)

### Phase 4-5 — Minimal questioning (mostly assembly from earlier answers)

### Phase 6 (Operations) — Event-driven, not pre-clustered

---

## Anti-Patterns

- ❌ **20-question interrogation.** Never present more than 5 questions in a single turn. If you need more, present 3-5, get answers, then ask the next batch.
- ❌ **Re-asking known information.** If the PIP says "5 stakeholders" — don't ask "how many stakeholders?" Read the input first.
- ❌ **Questions without context.** Never ask "What's your release strategy?" without explaining why it matters and what the options mean.
- ❌ **Binary questions when options exist.** Don't ask "Do you want WSJF?" — present the landscape and let the user choose.
- ❌ **Deferring all decisions.** If the user hasn't specified, recommend based on context factors. Don't keep asking "what would you like?" — propose and let them adjust.

---

## Depth-Adapted Questioning

| Depth | Question Behavior |
|-------|------------------|
| **Minimal** | Ask only 🔴 Required questions. Use defaults for everything else. State the defaults used. |
| **Standard** | Ask 🔴 + 🟡 questions. Offer options for all key decisions. |
| **Comprehensive** | Full exploration. Present multiple options with detailed trade-offs. Explore edge cases. Ask about exceptions and special scenarios. |

---

*Load this file at workflow start. Reference it whenever gathering user input.*
