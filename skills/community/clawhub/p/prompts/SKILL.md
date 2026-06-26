---
name: prompts
description: Deep prompt engineering workflow—task spec, constraints, examples, evaluation sets, iteration protocol, regression testing, and safety alignment. Use when improving LLM outputs, shipping prompt changes, or building reusable prompt templates.
---

# Prompt Engineering (Deep Workflow)

Prompts behave like **natural-language programs**: they need **specs**, **tests**, and **version control**—especially in production.

## When to Offer This Workflow

**Trigger conditions:**

- Prompt or system message change; quality regressions
- Structured outputs (JSON), tool use, or RAG grounding requirements
- Safety or policy alignment needs

**Initial offer:**

Use **six stages**: (1) define task & success, (2) constraints & format, (3) few-shot & style, (4) build eval set, (5) iterate with discipline, (6) ship, monitor, regress). Confirm model family and latency budget.

---

## Stage 1: Define Task & Success

**Goal:** Clear user-visible outcome and failure modes (hallucination, omission, tone).

**Exit condition:** Success rubric in plain language; out-of-scope cases listed.

---

## Stage 2: Constraints & Format

**Goal:** Must/must-not rules; output schema (JSON Schema, bullet structure); length limits.

### Practices

- Separate system (policy, role) from user (task instance)
- Ask model to cite sources when grounding matters

---

## Stage 3: Few-Shot & Style

**Goal:** Use examples only when they reduce ambiguity—avoid huge prompt bloat.

### Practices

- Diverse examples; avoid overlong negative examples that confuse

---

## Stage 4: Build Eval Set

**Goal:** Frozen inputs with expected properties (not always exact text match).

### Practices

- Adversarial and multilingual slices if relevant
- Regression suite in CI for critical prompts

---

## Stage 5: Iterate With Discipline

**Goal:** Change one major variable at a time when debugging quality.

### Practices

- Compare with same temperature settings when A/B testing wording
- Log prompt version id with outputs in production

---

## Stage 6: Ship, Monitor, Regress

**Goal:** Canary prompt changes; watch implicit signals (thumbs, edits, task completion).

---

## Final Review Checklist

- [ ] Task and rubric defined
- [ ] Constraints and output format explicit
- [ ] Eval set versioned; regression path exists
- [ ] Iteration log disciplined; prompt versions tracked
- [ ] Production monitoring and rollback plan

## Tips for Effective Guidance

- Clarity beats cleverness—short explicit instructions often win.
- Chain-of-thought: use when reasoning helps; hide chain from end users if needed.
- Align with **llm-evaluation** skill for larger harness design.

## Handling Deviations

- **Chat** vs **batch**: batch can use stricter structure and lower temperature.
- **Multimodal**: specify how image details may be used or ignored.
