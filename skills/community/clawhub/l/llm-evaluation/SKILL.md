---
name: llm-evaluation
description: Deep LLM evaluation workflow—quality dimensions, golden sets, human vs automatic metrics, regression suites, offline/online signals, and safe rollout gates for model or prompt changes. Use when shipping prompt updates, swapping models, or building eval harnesses for agents and RAG.
---

# LLM Evaluation (Deep Workflow)

Evaluation turns “it feels better” into **reproducible evidence**. Design around **failure modes** your product cares about—not only aggregate scores.

## When to Offer This Workflow

**Trigger conditions:**

- Prompt or model change; need **before/after** proof
- Building **CI** for LLM outputs; flaky quality in production
- RAG/agents: **grounding**, **tool use**, **safety** regressions

**Initial offer:**

Use **six stages**: (1) define quality & constraints, (2) build datasets & rubrics, (3) automatic metrics, (4) human evaluation, (5) regression & gates, (6) online validation & iteration. Confirm **latency/cost** budgets and **risk** (PII, safety).

---

## Stage 1: Define Quality & Constraints

**Goal:** Name **dimensions** that map to user harm if they fail.

### Typical dimensions (pick what matters)

- **Correctness** / task success; **groundedness** (RAG); **faithfulness** to sources
- **Safety**: policy violations, jailbreaks, PII leakage
- **Style**: tone, brevity, format (when product-critical)
- **Robustness**: paraphrase, multilingual, edge inputs

### Constraints

- Max **tokens**, **latency** p95, **cost** per request; **locale** requirements

**Exit condition:** Weighted **priority** of dimensions; **non-goals** stated.

---

## Stage 2: Datasets & Rubrics

**Goal:** **Fixed** eval sets + **clear** scoring rules.

### Practices

- **Stratify** by intent: easy/medium/hard; **adversarial** slice separate
- **Rubrics**: 1–5 scales with **anchors**; **binary** checks for safety
- **Version** datasets (git or table); **no** silent edits without changelog
- **Privacy**: synthetic or **redacted** real examples per policy

**Exit condition:** **Golden set** size justified; **inter-rater** plan if human scoring.

---

## Stage 3: Automatic Metrics

**Goal:** **Fast** signals—know **limitations**.

### Options

- **Reference-based**: BLEU/ROUGE—often weak for assistants
- **Model-as-judge**: fast, biased—**calibrate** vs human
- **Task-specific**: exact match, JSON schema validity, tool-call args match
- **RAG**: citation overlap, **nugget** recall, entailment models (use carefully)

### Hygiene

- **No** training on test; **detect** **leakage** from prompts

**Exit condition:** Each auto metric has **known blind spots** documented.

---

## Stage 4: Human Evaluation

**Goal:** **Authoritative** judgment where automatic metrics lie.

### Design

- **Sample size** for confidence; **blind** A/B when possible
- **Guidelines** + **examples**; **adjudication** for disagreements
- **Locale-native** raters when language quality matters

**Exit condition:** **Human** scores correlate **enough** with auto for ongoing monitoring—or you rely on human for release.

---

## Stage 5: Regression & Gates

**Goal:** **Block** bad deploys in **CI** or **release** pipeline.

### Gates

- **Must-pass** suites: safety, critical user journeys
- **Trend** tracking: **not** only point-in-time
- **Canary** with **online** metrics (see Stage 6)

### Artifacts

- **Report**: model/prompt id, dataset versions, scores, **diff**

**Exit condition:** **Rollback** criteria defined before rollout.

---

## Stage 6: Online Validation

**Goal:** **Production** truth—shadow, A/B, or gradual ramp.

### Signals

- **Implicit**: thumbs, edits, task completion, support tickets
- **Explicit**: user ratings (sparse)

### Causality

- **Confounds**: seasonality, cohort—**control** where possible

---

## Final Review Checklist

- [ ] Quality dimensions prioritized for the product
- [ ] Versioned eval sets and rubrics
- [ ] Auto + human roles explicit; limitations documented
- [ ] Release gates and rollback tied to metrics
- [ ] Plan for online feedback loop

## Tips for Effective Guidance

- **Slice** metrics—averages hide **regressions** on critical intents.
- For **agents**, evaluate **trajectories**, not only final text.
- Never claim **objective** truth—evaluation is **operationalized** judgment.

## Handling Deviations

- **No labels**: start with **smallest** **pairwise** comparison set + **spot** human review.
- **High-stakes** (medical/legal): **human-in-the-loop** gate; disclaim **limits** of auto eval.
