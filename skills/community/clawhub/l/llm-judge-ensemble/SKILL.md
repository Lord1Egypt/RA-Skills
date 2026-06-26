---
name: llm-judge-ensemble
version: 1.0.1
description: Build a cost-efficient LLM evaluation ensemble with sampling, tiebreakers, and deterministic validators. Learned from 600+ production runs judging local Ollama models.
homepage: https://github.com/reddinft/skill-llm-as-judge
metadata:
  {
    "openclaw": {
      "emoji": "⚖️",
      "requires": {
        "bins": ["python3", "ollama"],
        "env": ["ANTHROPIC_API_KEY", "OPENAI_API_KEY"]
      },
      "primaryEnv": "ANTHROPIC_API_KEY",
      "network": {
        "outbound": true,
        "reason": "Calls Anthropic (Claude Sonnet) and OpenAI (GPT-4o-mini) as judge models at 15% sampling rate. Optional Gemini tiebreaker. Local model inference via Ollama stays on-device."
      },
      "security_notes": "All LLM API calls are made using the user's own API keys to providers they have accounts with. No data is sent to third parties beyond the user's chosen LLM providers (Anthropic, OpenAI, Google). Judge sampling is at 15% — the majority of evaluation runs never make external API calls."
    }
  }
---
**Last used:** 2026-03-24
**Memory references:** 1
**Status:** Active


# LLM-as-Judge

Build a cost-efficient LLM evaluation ensemble for comparing and scoring generative AI outputs at scale.

---

## When to Use This / When NOT to Use This

**Use LLM-as-Judge when:**
- Evaluating generative AI outputs across multiple models at scale (100+ runs)
- Comparing local/OSS models against cloud baselines in shadow-testing pipelines
- Building promotion gates where models must prove quality before serving production traffic
- Any scenario where deterministic tests alone can't capture output quality
- You need a structured, reproducible score with documented rubric criteria

**Do NOT use LLM-as-Judge when:**
- One-off evaluations (just read the output yourself)
- Tasks with deterministic correct answers (use exact-match or unit tests)
- When you can't afford any external API calls (this pattern uses Claude/GPT as judges)
- You need a fast yes/no QA gate on a single PR or file change — see below

### LLM-as-Judge vs Oli QA Gate

These two evaluation approaches overlap but serve different purposes:

| | LLM-as-Judge (this skill) | Oli QA Gate |
|---|---|---|
| **What it evaluates** | Model output quality across many runs | A specific build, PR, or code change |
| **Scale** | 100–1000s of outputs, statistical view | Single task, single output |
| **Rubric** | Multi-dimension, configurable weights | Oli's built-in code/content quality checklist |
| **Cost model** | 15% sampling to control spend | One-shot review, no sampling |
| **When to use** | Model comparison, shadow testing, promotion gates | Post-Kit build review, content QA before publish |
| **Output** | Weighted numeric score + dimension breakdown | Pass/Fail with specific feedback items |

**Rule:** If you're evaluating *a model's outputs at scale* → LLM-as-Judge. If you're reviewing *a specific piece of work* → Oli.

---

## Architecture: Three-Layer Evaluation

### Layer 1: Deterministic Validators (Free, Instant)

Run on 100% of outputs. Zero cost. Catches obvious failures before burning judge tokens.

- **JSON schema validation** — does the output parse? Does it match the expected schema?
- **Regex checks** — required fields present, format constraints met
- **Length bounds** — output within acceptable min/max character count
- **Entity presence** — do required entities from the input appear in the output?

If Layer 1 fails, score is 0.0 — no need to invoke expensive judges.

### Layer 2: Heuristic Drift Detection (Cheap, Fast)

Run on 100% of outputs that pass Layer 1. Minimal cost (local computation only).

- **Entity overlap** — what fraction of entities in the ground truth appear in the candidate?
- **Numerical consistency** — do numbers in the output match source data?
- **Novel fact detection** — does the output introduce facts not present in the input/context? Novel facts suggest hallucination.
- **Structural similarity** — does the output follow the same structural pattern as ground truth?

Layer 2 produces heuristic scores (0.0–1.0) that contribute to the final weighted score.

### Layer 3: LLM Judges (Expensive, High Quality)

**Sampled at 15% of runs** to control cost. Forced to 100% during promotion gates.

Two independent judges (e.g., Claude + GPT-4o) score the output. Each judge evaluates all 6 dimensions independently.

**Tiebreaker pattern:** When primary judges disagree by Δ ≥ 0.20 on any dimension, a third judge is invoked. The tiebreaker score replaces the outlier. This reduced score variance by 34% at only 8% additional cost.

---

## The 6 Scoring Dimensions

| Dimension | Weight | What It Measures |
|---|---|---|
| Structural accuracy | 0.20 | Format compliance, schema adherence |
| Semantic similarity | 0.25 | Meaning preservation vs ground truth |
| Factual accuracy | 0.25 | Correctness of facts, numbers, entities |
| Task completion | 0.15 | Does it actually answer the question? |
| Tool use correctness | 0.05 | Valid tool calls (when applicable) |
| Latency | 0.10 | Response time within acceptable bounds |

Weights are configurable per task type. Tool use weight is redistributed when not applicable.

---

## Minimum Viable Rubric (3-Criterion Example)

If you're building a new judge, start here. A rubric needs at minimum: criterion name, description, scoring anchor points, and weight.

```python
SUMMARISATION_RUBRIC = [
    {
        "criterion": "factual_accuracy",
        "description": "All facts, numbers, and named entities in the summary are present and correct relative to the source document.",
        "weight": 0.40,
        "anchors": {
            1: "Multiple factual errors or hallucinated entities",
            5: "Mostly accurate with minor omissions",
            10: "Fully accurate — every fact traceable to the source"
        }
    },
    {
        "criterion": "completeness",
        "description": "The summary covers the key points of the source without omitting critical information.",
        "weight": 0.35,
        "anchors": {
            1: "Covers less than half the key points",
            5: "Covers main points, misses some secondary ones",
            10: "Comprehensive — all key points captured"
        }
    },
    {
        "criterion": "conciseness",
        "description": "The summary avoids redundancy and filler. Information density is high.",
        "weight": 0.25,
        "anchors": {
            1: "Bloated — repetition or filler makes up >30% of the text",
            5: "Acceptable density with some redundancy",
            10: "Every sentence carries unique information"
        }
    }
]
```

**Anchor points are mandatory.** Without concrete score anchors, judges will default to the centre of the scale (all 5s or all 7s). See Score Calibration below.

---

## Score Calibration: Avoiding All 7s or All 10s

LLM judges are prone to centrality bias (clustering around the middle) and leniency bias (inflating scores). Counter these with:

**1. Forced anchor examples in the rubric prompt:**
Include 1–2 concrete output examples at score 2 and score 9 for each criterion. Judges calibrate against examples, not abstract descriptions.

**2. Require justification before score:**
Prompt: *"First write a 1-sentence critique, then give your score."* Chain-of-thought before the number reduces leniency bias significantly.

**3. Watch for score compression on small datasets:**
If all outputs score 7.2–7.8 on a 10-point scale, your rubric criteria may be too vague or your ground truth is low-quality. Tighten anchor definitions or add adversarial examples.

**4. Calibration run before production:**
Before trusting a new rubric, manually score 10 outputs, then compare to judge scores. If the correlation is below 0.7, rewrite the weakest criterion's anchor points.

**5. Normalise by judge:**
Different judges have different baseline biases. Track each judge's mean score across a calibration set and apply a per-judge offset if needed.

```python
# Example: detect and log judge bias
calibration_scores = {
    "claude": [7.2, 7.4, 7.1, 7.5, 7.3],  # compressed range → leniency bias
    "gpt4o":  [5.1, 8.3, 6.7, 9.1, 4.2],  # wider spread → better discrimination
}
for judge, scores in calibration_scores.items():
    spread = max(scores) - min(scores)
    print(f"{judge}: spread={spread:.1f}, mean={sum(scores)/len(scores):.1f}")
# If spread < 3.0 on a 10-point scale, that judge has calibration problems
```

---

## What Makes a Bad Rubric

Avoid these patterns — they produce noisy, unreliable scores:

| Anti-pattern | Example | Why it fails |
|---|---|---|
| **Compound criterion** | "Accurate AND well-written AND concise" | Judge can't assign one score to three things |
| **Vague superlatives** | "Is the response excellent?" | No anchor for what "excellent" means |
| **Overlapping criteria** | Separate "clarity" and "readability" | Judges score the same thing twice, inflating that dimension |
| **No anchor points** | "Score 1–10 for quality" | Produces centrality bias — everyone gets 5–7 |
| **Unmeasurable criterion** | "Does the response feel right?" | Subjective, inconsistent across judge models |
| **Too many criteria** | 12+ dimensions | Attention degrades, later criteria scored worse than early ones |

**Good rubric shape:** 3–6 criteria, each independently measurable, each with explicit anchor examples at the low, mid, and high end of the scale.

---

## Critical Lesson: None ≠ 0.0

When a dimension is not sampled (LLM judge not invoked on this run), record the score as **null**, not 0.0. Unsampled dimensions must be **excluded from the weighted average**, not treated as failures.

Early bug: recording unsampled dimensions as 0.0 created a systematic 0.03–0.08 downward bias across all models. The fix: null means "not measured", which is fundamentally different from "scored zero".

```python
# WRONG — penalises unsampled dimensions
weighted = sum(s * w for s, w in zip(scores, weights)) / sum(weights)

# RIGHT — exclude null dimensions
pairs = [(s, w) for s, w in zip(scores, weights) if s is not None]
weighted = sum(s * w for s, w in pairs) / sum(w for _, w in pairs)
```

---

## Cost Estimate

With 15% LLM sampling, average cost per evaluated run: **~$0.003**

- Layer 1 + Layer 2: $0.00 (local computation)
- Layer 3 (15% of runs): ~$0.02 per judged run × 0.15 = ~$0.003
- Tiebreaker (fires ~12% of judged runs): adds ~$0.0003

At 200 runs for promotion: total judge cost ≈ $0.60 per model per task type.

---

## Worked Example: Summarisation Evaluation

```python
from evaluation import JudgeEnsemble, DeterministicValidator, HeuristicScorer

# Layer 1: must be valid text, 50-500 chars
validator = DeterministicValidator(
    min_length=50,
    max_length=500,
    required_format="text",
)

# Layer 2: check entity overlap with source
heuristic = HeuristicScorer(
    check_entity_overlap=True,
    check_novel_facts=True,
    check_numerical_consistency=True,
)

# Layer 3: LLM judges (sampled)
ensemble = JudgeEnsemble(
    judges=["claude-sonnet-4-20250514", "gpt-4o"],
    tiebreaker="claude-sonnet-4-20250514",
    sample_rate=0.15,
    tiebreaker_threshold=0.20,
    dimensions=["structural", "semantic", "factual", "completion", "latency"],
)

# Evaluate
result = ensemble.evaluate(
    task_type="summarize",
    ground_truth=gt_response,
    candidate=candidate_response,
    source_text=original_text,
    validator=validator,
    heuristic=heuristic,
)

print(f"Weighted score: {result.weighted_score:.3f}")
print(f"Dimensions: {result.scores}")  # {semantic: 0.95, factual: 0.88, ...}
# None values for unsampled dimensions
```

---

## Tips

- **Start with Layer 1** — you'd be surprised how many outputs fail basic validation
- **Log everything** — store raw judge responses for debugging score disputes
- **Calibrate on 50 runs** — before trusting the ensemble, manually review 50 outputs against judge scores
- **Watch for judge drift** — LLM judges can be inconsistent across API versions; pin model versions
- **Force judges at gates** — 15% sampling is fine for monitoring, but promotion decisions need 100% coverage on the final batch

---

## Common Mistakes

1. **Recording unsampled dimensions as 0.0 instead of null**
   - Creates systematic downward score bias — see the None ≠ 0.0 section above

2. **No anchor points in rubric → all scores cluster at 7**
   - Every rubric criterion needs concrete examples at low (1–3), mid (4–6), and high (7–10)

3. **Compound criteria ("accurate AND clear AND concise")**
   - Split into separate criteria. Judges can't reliably score three things with one number.

4. **Running 15% sampling at promotion gates**
   - Production monitoring: 15% is fine. Promotion decisions: force 100% coverage on the final batch.

5. **Not pinning judge model versions**
   - `claude-sonnet-4` scoring patterns can shift between API versions. Pin the model string and update consciously.

6. **Rubric criteria that overlap**
   - "Clarity" and "Readability" are almost the same thing. Overlapping criteria inflate that quality dimension's effective weight.

7. **Skipping Layer 1 to "save time"**
   - Layer 1 is free and instant. Outputs that fail basic validation don't need an expensive LLM review. Always run validators first.
