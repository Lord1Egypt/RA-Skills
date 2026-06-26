---
name: interrogate
version: 1.0.0
description: >
  Guided elicitation skill. Activates ONLY when the user explicitly types /interrogate.
  Asks 4–15 adaptive questions in batches of 2, each with exactly 4 lettered options (A/B/C/D)
  plus an implicit 5th option where the user can write a free-text answer instead.
  Used to clarify vague or complex requests before acting, so the output matches
  exactly what the user actually wants.
---

# Interrogate

Activated by: `/interrogate` (literal command only — do not trigger on vague requests unless user types it)

## Flow

### 1. Detect complexity
On `/interrogate`, read the rest of the message (if any) to understand the topic.
If no topic is given, ask: *"What are we figuring out?"* before starting questions.

### 2. Ask in batches of 2
- Present **2 questions at a time**, each with options **A / B / C / D**
- Always add a silent 5th option: user can ignore the letters and write freely — handle that naturally
- After each batch of answers, decide:
  - Is the picture clear enough? → go to step 3
  - Need more clarity? → ask the next batch (max ~7 batches / ~15 questions total)
- Keep questions tight and mutually exclusive — no overlap between options

### 3. Confirm before acting
When enough is understood, summarize in 3–5 bullet points:
- What the user wants
- Key constraints or preferences gathered
- Anything still ambiguous (flag it)

Then ask: *"Does this match what you have in mind? Say yes to proceed, or correct anything."*

Only act after confirmation.

## Question Design Rules
- Options should be meaningfully different — not just degrees of the same thing
- One option can always be "Something else entirely" if the space is truly open
- Avoid leading questions — present options neutrally
- Adapt next batch based on previous answers (tree-style branching, not fixed sequence)
- For creative tasks: first batch should explore tone/style/audience
- For technical tasks: first batch should explore scope/constraints/output format
- For decisions/planning: first batch should explore goal/timeline/constraints

## Format
```
**Q1. [Question]**
A) Option one
B) Option two
C) Option three
D) Option four

**Q2. [Question]**
A) Option one
B) Option two
C) Option three
D) Option four

*(Or just write what's on your mind — I'll adapt)*
```

## Example opening batches

**Creative task** (`/interrogate I want a landing page`):
- Q1: What's the primary goal of this page? A) Capture emails B) Explain a product C) Drive a purchase D) Build credibility
- Q2: What's the tone? A) Clean and minimal B) Bold and energetic C) Warm and human D) Technical and precise

**Vague task** (`/interrogate`):
- Ask "What are we figuring out?" first, then branch from the answer

## When the user is undecided
If the user answers with "maybe", "not sure", "probably X or Y", or picks multiple options — **do not re-ask**. Instead:
1. Briefly explain the key difference between the options they're torn between (1-2 sentences each)
2. Add concrete trade-offs: cost, complexity, maintenance, limitations
3. Give a clear recommendation based on context ("Given X, I'd go with B")
4. Then let them confirm or override

Example: user says "A probably or maybe C"
→ "A (Railway URL) means it's always accessible from anywhere, zero effort, but uses a port on your Railway service. C (local/on-demand) means zero ongoing resource cost but you'd need to spin it up manually. Given you're already on Railway and want it always-on, I'd go with A."

Never leave the user hanging on a decision they don't have enough info to make.

## Ending early
If the user gives a very detailed free-text answer at any point that makes further questions unnecessary, skip remaining questions and jump straight to the confirmation summary.
