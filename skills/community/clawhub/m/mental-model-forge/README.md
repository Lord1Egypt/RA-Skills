# Mental Model Forge

> **F.A.C.E.T. framework** for extracting reusable mental models from books and theories. Turns abstract concepts into strategic weapons you can apply today.

---

## What It Does

Extracts **reusable mental models** from books using the **F.A.C.E.T. framework**:

- **[F] Framework** — Core mechanism in ≤50 words (EN) / ≤80 chars (CN)
- **[A] Anchor Case** — Most iconic real-world example (vivid story that sticks)
- **[C] Contradiction** — What "common sense" does this destroy?
- **[E] Edge** — When does this model fail? Hidden assumptions?
- **[T] Transfer** — Map to YOUR reality TODAY (personalized from USER.md)

**Not a book summary** — A battle-tested mental model you can apply across domains.

---

## Quick Start

### Install

```bash
clawhub install mental-model-forge
```

### Use It

```
Ask your AI: "Use F.A.C.E.T. framework to analyze: 'The Innovator's Dilemma' by Clayton Christensen"
```

**Output**:

```markdown
### 💎 Disruptive Innovation

- **[F] Core Framework**: Incumbents optimize for high-margin customers →
  Ignore low-end market → Startups enter with "worse but cheaper" →
  Improve quality over time → Displace incumbents.

- **[A] Anchor Case**: 14-inch hard drive giants chased mainframe capacity →
  Ignored 5.25-inch drives → Desktop PCs adopted small drives →
  Quality improved → 5.25-inch killed the 14-inch market.

- **[C] Contradiction**: "Listen to your best customers" is wrong.
  Best customers lead you to death — they want sustaining innovation,
  not disruptive.

- **[E] Edge**: Fails when tech improvement < demand growth (e.g., battery
  energy density). Also fails for high-end disruption (Tesla).

- **[T] Transfer**: Map to your current projects — are you serving
  "highest quality customers" or exploring "edge markets"?

### ⚡ Strategic Question
In your projects, are you competing on "better" (sustaining) or
"cheaper + more accessible" (disruptive)?
```

---

## Why F.A.C.E.T. Works

### [F] — Not a Summary, a Skeleton
**Bad**: "The book talks about how incumbents fail..."
**Good**: "Incumbents optimize → Ignore low-end → Startups enter → Displace"

The second one is **actionable** — you can apply it to any market.

### [A] — Anchor Case = Memory Glue
Abstract theory forgets in 1 week. A vivid story remembers forever.
"14-inch hard drives killed by 5.25-inch" — that sticks.

### [C] — Contradiction = Mental Shift
Every great model **destroys a common belief**. F.A.C.E.T. forces you to identify the contrarian insight.

### [E] — Edge = Intellectual Honesty
Bad notes: "This theory is amazing!"
F.A.C.E.T. [E]: "Fails when X, Y, Z assumptions break."

### [T] — Transfer = Personalization
Generic: "Applies to business strategy."
F.A.C.E.T. [T]: "For YOU, this means: compete on accessibility, not accuracy."

**How it works**: Reads your `USER.md` → Maps theory to YOUR job/projects/challenges.
If no USER.md exists, provides general transfer suggestions using "you".

---

## Use Cases

### 1. Build Your Mental Model Library (with cognitive-forge)
`cognitive-forge` calls `mental-model-forge` daily → Writes to `thinking-patterns.md`.
Over time: 100 books = 100 reusable frameworks.

### 2. Deep Book Comprehension
After reading a book, run F.A.C.E.T. analysis to extract actionable mental models.

### 3. Research Literature Review
Analyze multiple books → Extract core models → See how they agree, conflict, or complement.

### 4. Team Learning System
Share F.A.C.E.T. analyses → Build shared mental model language across teams.

---

## Context-Specific Transfer

The [T] Transfer dimension becomes more powerful with a detailed `USER.md`:

**Generic USER.md** → Generic transfer: "Apply to product design"

**Detailed USER.md** (profession, projects, challenges) → Specific transfer: "Your AI assistant has low engagement because of System 1 friction. Reduce onboarding steps from 5 → 1."

---

## File Structure

```
mental-model-forge/
├── SKILL.md    # F.A.C.E.T. framework definition
└── README.md   # This file
```

Super lightweight. No dependencies.

---

## Troubleshooting

**"Analysis is too shallow"**:
- Provide more context (book excerpts, specific chapters)
- Ask: "Deep F.A.C.E.T. analysis with multiple examples"

**"[T] Transfer is too generic"**:
- Update your `USER.md` with more specific details
- Ask: "Tailor [T] to my exact situation: [describe your challenge]"

**"Can this work for research papers?"**:
- Yes. F.A.C.E.T. extracts the core model, not the data/results.

---

## License

MIT-0

---

*Version: 3.1.0*
*Last updated: 2026-03-27*
*Changes: Removed hardcoded user references, aligned version with SKILL.md, added interface clarity*
