# Paper Reading Socratic Coach 🧠

A diagnostic-first OpenClaw / ClawHub skill for training **independent paper reading ability**, **scientific thinking**, and **research methodology judgment**.

This skill is built for a very specific goal:

> help the learner read papers well **without becoming permanently dependent on AI**.

Instead of directly summarizing a paper for the user, the skill first builds a teacher-side reference understanding, then produces a **Precision Report**, and only after that starts an adaptive question loop using **single-choice**, **multi-select**, and **short-answer** questions.

It tracks three long-term abilities:

- **Reading**: can the learner reconstruct what the paper actually says?
- **Thinking**: can the learner reason about design choices, claims, evidence, and alternatives?
- **Methodology**: can the learner judge whether the evidence, experiments, and theory really support the conclusions?

---

## Why this skill exists

Many paper-reading tools do one of two things:

1. summarize papers too aggressively, which weakens the learner's own reconstruction ability;
2. ask generic “what is the contribution?” questions, which are too shallow to expose real weaknesses.

This skill is designed to be stricter.
It first creates a **diagnostic hypothesis** about the learner's likely weak points, then asks questions that test:

- paper-grounded understanding
- equation / module interpretation
- experiment-purpose understanding
- claims-evidence alignment
- weakness detection
- future-direction generation

Every answer updates a persistent learning state, so the next session can resume from earlier weaknesses instead of starting from zero.

---

## Design inspirations

This package was shaped by four design ideas:

1. **Deep-reading rigor**: preserve formulas, module details, experiments, assumptions, and claim-evidence mapping.
2. **Guided training**: use adaptive questions instead of one-shot explanation.
3. **Reviewer-style critique**: diagnose unsupported reasoning, weak evidence reading, and overclaiming.
4. **Stateful continuation**: keep a running mastery record and continue from it next time.

---

## Best use cases

Use this skill when you want to:

- train yourself to read papers independently
- prepare for group meeting / lab discussion
- stress-test whether you really understand a paper
- identify whether your weakness is in reading, thinking, or methodology
- build long-term scientific reading habits
- turn one paper into a training curriculum

---

## Input options

You can start from:

- a PDF
- a LaTeX source bundle
- a paper title
- an arXiv / DOI / OpenReview link
- a paper plus your old learning state

Preferred source order for teacher-side analysis:

1. LaTeX source
2. user-uploaded PDF
3. official paper page / official PDF
4. arXiv
5. OpenReview (when relevant)

---

## Core workflow

### 1. Teacher-side reference pass
The skill first reconstructs the paper internally using a deep-reading lens.
This is for calibration, not for replacing the learner's reading.

### 2. Precision Report first
Before asking many questions, the skill outputs a **Precision Report** with:

- prior-state carryover
- pre-question diagnostic hypothesis
- planned question mix
- target difficulty
- session goals

### 3. Adaptive questioning
The skill then asks a sequence of questions such as:

- single-choice
- multi-select
- short answer
- evidence retrieval
- methodology critique
- future-direction generation

### 4. Per-answer diagnosis
After each answer, it reports:

- what is right
- what is missing
- which paper evidence matters
- which weakness category was exposed
- how the learning state changes

### 5. Persistent learning-state update
At the end of each session, it updates:

- dimension scores
- recurring error patterns
- next practice focus
- recommended next difficulty

---

## Learning state files

This skill is designed to use a workspace-level state folder:

```text
.paper-reading-coach/
  learning_state_latest.md
  session_log.md
```

Why not store state inside the skill folder itself?
Because skill folders may be updated or replaced when you install a new version. A workspace-level state directory is safer for long-term learning records.

If the agent can write files, it should update those files automatically.
If not, it should print the full state block so you can save it manually.

Templates are included in `templates/`.

---

## File structure

```text
paper-reading-socratic-coach-openclaw/
├─ SKILL.md
├─ README.md
├─ LICENSE
├─ docs/
│  └─ publishing_to_clawhub.md
├─ rubrics/
│  ├─ precision_dimensions.md
│  └─ weakness_taxonomy.md
├─ templates/
│  ├─ precision_report_template.md
│  ├─ learning_state_template.md
│  └─ session_log_template.md
└─ examples/
   └─ example_session_cn.md
```

---

## Quick start

### Example 1 — first diagnostic session

```text
Train me on this paper. Start with a precision report, then quiz me.
[paste title / upload PDF / provide arXiv link]
```

### Example 2 — continue from previous state

```text
Use my previous learning state and continue the paper reading drill on this new paper.
```

### Example 3 — methodology-focused session

```text
Train me on this paper, but focus on experiment interpretation, claims-evidence alignment, and methodology.
```

### Example 4 — question-format control

```text
Use only multi-select and short-answer questions in this session.
```

### Example 5 — frontier extension after basic understanding

```text
After checking that I understand the paper, test whether I can propose serious follow-up directions.
```

---

## Example interaction (Chinese)

See:

- `examples/example_session_cn.md`

That file shows a full session skeleton:

- Precision Report
- first question
- answer feedback
- learning-state delta
- end-of-session update

---

## What makes this different

This skill is deliberately **not** a pure paper summarizer.
It behaves more like a strict tutor + reviewer + research-method coach.

It distinguishes between errors like:

- “you did not read closely enough”
- “you understood the words but not the logic”
- “you can restate the method but cannot judge evidence quality”
- “you can criticize the paper but cannot reconstruct the authors' reasoning path”

That distinction is crucial if the goal is long-term growth.

---

## Score system

The skill tracks 10 dimensions from 0–5:

1. Problem understanding
2. Title-to-content interpretation
3. Related-work relation mapping
4. Method reconstruction
5. Formula / theorem interpretation
6. Experiment interpretation
7. Claims-evidence alignment
8. Weakness and limitation detection
9. Future-direction generation
10. Scientific methodology awareness

It also maintains three macro scores:

- **Reading**
- **Thinking**
- **Methodology**

---

## Recommended usage pattern

A strong routine is:

1. choose one paper;
2. do one diagnostic-first session;
3. save the updated learning state;
4. return later for a continuation session;
5. periodically switch to a harder paper or a new subfield.

You can also run focused sessions such as:

- formula-only drill
- experiment-only drill
- related-work mapping drill
- frontier-generation drill

---

## Publishing notes

This bundle is intentionally **text-only** and lightweight to make it easier to inspect, version, and publish to ClawHub.

Before publishing, replace the placeholder homepage in `SKILL.md` with your real GitHub repository URL.

See:

- `docs/publishing_to_clawhub.md`

---

## Suggested GitHub repo topics

```text
openclaw-skill
clawhub
research-skill
paper-reading
socratic-learning
academic-reading
research-methodology
study-skill
```

---

## License

Use **MIT-0** if you plan to publish this exact bundle to ClawHub so the repository license matches the registry distribution model.
