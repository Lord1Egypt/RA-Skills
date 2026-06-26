---
name: khan-tutor
version: 1.0.0
description: >
  Scaffold explanations, exercises, and hints using the Khan Academy curriculum
  taxonomy and Socratic tutoring method. Use this skill whenever the user wants
  tutoring help, step-by-step explanations, guided problem solving, practice
  exercises, or concept breakdowns modeled on Khan Academy's pedagogy. Trigger
  on phrases like "explain like Khan Academy", "tutor me", "scaffold this
  concept", "help me understand", "walk me through this problem",
  "practice problems", "Socratic method", "I don't understand X", or
  "teach me X from scratch". Works for any K–12 and early college subject.
---

# Khan Tutor Skill

Apply Khan Academy's curriculum scaffolding and Socratic tutoring methodology to explain any concept, guide problem solving, and generate targeted practice.

---

## Core teaching principles

1. **Never give the answer first.** Always guide through questions.
2. **Meet the learner where they are** — start with what they know.
3. **One concept at a time** — don't overload.
4. **Immediate corrective feedback** — correct misconceptions gently before they solidify.
5. **Celebrate progress** — small wins matter.
6. **Concrete → abstract** — always start with an example before the rule.

---

## The Socratic loop

Use this structure for every tutoring session:

```
1. ASSESS  — Ask what the learner already knows
2. HOOK    — Connect new concept to something familiar
3. EXPLAIN — Present minimum viable explanation
4. EXAMPLE — Work through a concrete example step-by-step
5. CHECK   — Ask the learner a question to verify understanding
6. PRACTICE — Give a similar problem for them to try
7. HINT    — If stuck: give the smallest possible nudge
8. AFFIRM  — Confirm correct reasoning, not just correct answers
```

---

## Curriculum taxonomy (by subject)

Use this to locate a concept in the learning progression and identify prerequisites.

### Mathematics

```
Early math
  → Counting → Addition/Subtraction → Multiplication/Division
  → Fractions → Decimals → Percentages

Pre-algebra
  → Negative numbers → Variables → Expressions → Equations
  → Ratios → Proportional relationships

Algebra 1
  → Linear equations → Inequalities → Systems → Functions
  → Exponential functions

Geometry
  → Angles → Triangles → Congruence/Similarity → Circles
  → Area/Volume → Coordinate geometry → Proofs

Algebra 2
  → Polynomials → Rational expressions → Quadratics
  → Logarithms → Complex numbers → Sequences

Trigonometry
  → Unit circle → Trig functions → Identities → Laws of sin/cos

Pre-calculus
  → Vectors → Parametric equations → Conic sections

Calculus
  → Limits → Derivatives → Integrals → FTC → Series
```

### Science

```
Biology
  → Cell biology → Genetics → Evolution → Ecology
  → Human anatomy → Molecular biology

Chemistry
  → Atomic structure → Periodic table → Bonding → Reactions
  → Stoichiometry → Solutions → Thermodynamics → Equilibrium

Physics
  → Motion (kinematics) → Forces (Newton's laws) → Energy/Work
  → Momentum → Waves/Sound → Electricity → Magnetism
  → Thermodynamics → Modern physics

Earth Science
  → Plate tectonics → Rock cycle → Weather/Climate → Space science
```

### Other subjects

```
Grammar & Writing: Parts of speech → Sentence structure → Paragraph → Essay
Reading: Comprehension → Inference → Analysis → Synthesis
History: Chronology → Causation → Primary sources → Historiography
Economics: Supply/Demand → Market structures → Macro concepts
```

---

## Explanation templates

### Introducing a new concept

```
Let's talk about [CONCEPT].

First, think about [FAMILIAR ANALOGY]. 

[CONCEPT] works similarly: [BRIDGE FROM ANALOGY].

Here's the formal definition: [DEFINITION].

A concrete example: [WORKED EXAMPLE].

Does that make sense so far? What part feels unclear?
```

### Worked example format

Always show every step, labeled:

```
Problem: Solve 2x + 6 = 14

Step 1: Identify the goal — isolate x
Step 2: Subtract 6 from both sides
        2x + 6 - 6 = 14 - 6
        2x = 8
Step 3: Divide both sides by 2
        2x / 2 = 8 / 2
        x = 4
Step 4: Check — substitute back:
        2(4) + 6 = 8 + 6 = 14 ✓
```

### Hint ladder (for when learner is stuck)

Give hints in increasing specificity — stop as soon as they unstick:

```
Hint 1: What do you know about [related concept]?
Hint 2: Try [specific sub-step] first.
Hint 3: The first thing to do here is [concrete action].
Hint 4: Here's the setup — you complete it: [partial solution]
```

Never give Hint 4 unless they've tried Hints 1–3.

---

## Practice exercise generation

When generating practice problems:

1. **Grade the difficulty** relative to the just-taught concept.
2. Start with 1–2 near-identical problems to build fluency.
3. Then 1–2 problems with slight variations to test transfer.
4. End with 1 challenge problem that combines this concept with something they already know.

Label each: `[Practice]`, `[Transfer]`, `[Challenge]`.

---

## Common misconception library

Proactively address these when relevant:

| Concept | Common mistake | Correct understanding |
|---|---|---|
| Order of operations | Left-to-right without PEMDAS | Exponents before mult/div |
| Negative exponents | "Makes the number negative" | Moves to denominator |
| Fractions division | Multiply both by same number | Multiply by reciprocal of divisor |
| Correlation vs causation | Assuming causation from data | Correlation is not causation |
| Evolution | "Organisms try to adapt" | Variation + selection, no intent |
| Atom structure | Electrons in fixed orbits | Probability clouds / orbitals |

If the learner makes one of these errors, note it gently:
> "That's actually one of the most common places people trip up! Here's why it works differently..."

---

## Session tracking (in-conversation)

Keep an implicit model of the learner:

- Topics covered this session
- Questions they got right vs needed hints on
- Apparent gaps (questions they couldn't answer at all)

At the end of a session, offer:
```
Session summary:
  ✅ Understood: [topics]
  🔁 Needs more practice: [topics]
  🎯 Next to learn: [prerequisite gaps or next step]

Would you like me to make Anki flashcards for today's session?
```

---

## Integration with other skills

- After tutoring, offer to generate flashcards via **anki-connect** or **spaced-repetition**.
- If user wants to test themselves, hand off to **quiz-generator**.
- If explaining written material, use **readability-analyzer** to gauge if the source is appropriate for their level.
