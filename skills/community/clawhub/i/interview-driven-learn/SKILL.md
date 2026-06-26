---
name: interview-driven-learn
description: "Interview-driven is all you need. Drives end-to-end tech learning with interview standards. Activated when the user submits study notes, project summaries, or technical concept explanations. Transforms any learning input into interview-ready output using a five-step process: (1) Feynman test (ELI5 + professional), (2) interview question generation with answer points and follow-up traps, (3) STAR story extraction, (4) analogical learning, (5) weakness diagnosis. Auto-maintains two reference documents: a Knowledge Base (learning timeline) and a Question Bank (all questions aggregated by topic for self-review). Designed for computer science students preparing for backend, algorithm, or system design interviews at top internet companies."
---

# Interview Prep

> Start from the end: turn every learning session directly into interview readiness.

## Core Files

- **Knowledge Base**: `references/knowledge-base.md` — appended with each new topic, recording the theme + learning timestamp
- **Question Bank**: `references/question-bank.md` — all interview questions aggregated by topic for easy self-review

---

## Input

Any learning content submitted by the user: study notes, technical concepts, project descriptions, etc.

## Output: Five-Step Process

For every input, execute the following five steps:

---

### Step 1 - Feynman Test (ELI5 + Professional)

Describe the concept in two ways:
- **ELI5**: As if explaining to a 10-year-old
- **Professional**: Complete, rigorous, no key details omitted

Purpose: Verify true understanding, not rote memorization.

---

### Step 2 - Interview Question Generation

Generate 5-8 high-frequency interview questions in three categories:
- **Fundamentals** (what / differences / principles)
- **Deep Dive** (why / how / tradeoffs)
- **Applied** (examples / scenario-based)

Each question includes:
- What it tests
- Key answer points
- Follow-up direction if answered incorrectly

**→ Also append to `question-bank.md` (aggregated by topic)**

---

### Step 3 - STAR Story Extraction

Break down the content into reusable STAR narratives:
- **Situation**: Background (technical scenario / business constraints)
- **Task**: Goal (what you needed to solve)
- **Action**: What you specifically did
- **Result**: Quantified outcomes + lessons learned

Best for: project experiences, problem-solving stories, team collaboration.

---

### Step 4 - Analogical Learning (One to Three)

- **Same-level analogy**: What is this like in everyday life? What else works this way?
- **Deeper analogy**: What is one level below this? What's the underlying principle?
- **Transfer analogy**: Where else can this approach be applied?

Purpose: Build a knowledge network, not isolated facts.

---

### Step 5 - Weakness Diagnosis + Knowledge Archive

Proactively uncover vulnerabilities:
- Where will interviewers probe until you can't answer?
- What do you think is important but actually isn't?
- What classic pitfalls remain unfilled? (edge cases, concurrency, distributed tradeoffs)

**→ Append to `knowledge-base.md`** with format:

```markdown
## [Topic]
- Learned at: YYYY-MM-DD HH:mm
- Core takeaway: one-sentence summary
- Weak spots to reinforce: [spot 1, spot 2, ...]
```

---

## Output Format Template

```markdown
## 📚 Topic: [User's Input Topic]

---

### 1. Feynman Test

**ELI5:**
> [One-sentence version]

**Professional:**
> [Full description]

---

### 2. Interview Questions

| # | Question | Tests | Key Points |
|---|----------|-------|------------|
| Q1 |          |       |            |

**Follow-up traps:** ...

---

### 3. STAR Story

- **S**: [Background]
- **T**: [Goal]
- **A**: [Action]
- **R**: [Result + Reflection]

---

### 4. Analogical Learning

- 🔗 **Same-level**: ...
- 🔬 **Deeper**: ...
- 🚀 **Transfer**: ...

---

### 5. Weakness Diagnosis

⚠️ Likely follow-up pressure points:
1. ...
2. ...

---

*Synced to Knowledge Base & Question Bank*
```

---

## File Structure

```
interview-prep/
├── SKILL.md
└── references/
    ├── knowledge-base.md   # Learning timeline
    └── question-bank.md    # Interview questions by topic
```

---

## Trigger Words

When the user says/submits:
- "I learned XXX today"
- "Help me prepare for an interview"
- "Generate interview questions from these notes"
- "What interview questions can come from this concept"
- "What questions can this project be asked"

→ Activate this skill and run the five-step process, updating both documents.
