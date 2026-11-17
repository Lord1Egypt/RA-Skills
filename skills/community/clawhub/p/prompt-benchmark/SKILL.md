---
name: prompt-benchmark
description: Evaluate one or more prompts with an evidence-based static benchmark covering general quality, structure and format, few-shot examples, safety and robustness, target-model compatibility, and cross-model portability. Use when Codex needs to score, audit, lint, compare, or diagnose prompts; assess whether a prompt is production-ready; check examples or output schemas; identify model-specific assumptions; or recommend high-priority improvements without actually running the prompt against external models.
metadata:
  openclaw:
    requires:
      bins:
        - python3
---

# Prompt Benchmark

Produce a reproducible static assessment of a prompt. Separate universal prompt quality from target-model compatibility, and never present static predictions as measured runtime performance.

## Required inputs

Accept:

- the prompt text;
- an optional use case, audience, input shape, expected output, or success criteria;
- optional target model identifiers;
- optional comparison prompts.

If context is missing, continue with explicit assumptions when a useful assessment is still possible. Lower confidence or mark criteria `N/A` instead of inventing requirements. Ask a question only when the missing information would materially change the assessment.

Treat model family names such as `Claude`, `GPT`, or `DeepSeek` as underspecified. State that family-level advice is being given unless an exact model/version is supplied.

## Workflow

### 1. Frame the task

Identify the task type, intended user, input, expected output, constraints, risk level, and target model. Distinguish requirements stated by the user from assumptions made during evaluation.

Choose an applicable task profile from `references/scoring-rubric.md`. Use the default weights only when no better profile applies.

### 2. Run deterministic lint

For prompts available as text or files, run:

```bash
python3 {baseDir}/scripts/static_lint.py path/to/prompt.txt
```

Use `-` to read stdin and `--format markdown` for a readable summary. Treat script findings as leads, not final judgments: confirm each finding against the prompt before reporting it.

### 3. Evaluate the six modules

Read `references/scoring-rubric.md` completely and assess:

1. General quality
2. Structure and format
3. Few-shot quality
4. Safety and robustness
5. Target-model static compatibility
6. Cross-model compatibility

Apply only relevant criteria. Mark irrelevant criteria `N/A` and renormalize weights. Do not penalize a simple task merely for lacking a role, examples, XML tags, or a complex schema.

### 4. Ground every finding

For each material finding provide:

- status: `Pass`, `Warning`, `Fail`, or `N/A`;
- evidence: a short excerpt or precise location;
- impact: the likely execution consequence;
- recommendation: a concrete change;
- confidence: `High`, `Medium`, or `Low`.

Do not expose hidden chain-of-thought. Give concise evaluative reasons and observable evidence.

### 5. Score conservatively

Use the scoring anchors and severity caps in `references/scoring-rubric.md`.

- Keep universal quality and model compatibility scores separate.
- Do not reward verbosity or formatting complexity by itself.
- Avoid double-counting one root cause across modules. Assign the score impact to its primary module and cross-reference it elsewhere.
- Label model-specific scores as `Static compatibility prediction`.
- Label token cost, latency, hallucination rate, accuracy, and repeated-run consistency as `Not measured` unless actual runtime evidence was supplied.

### 6. Produce the report

Follow `references/report-schema.md`. Lead with the verdict, top risks, and highest-leverage fixes. Include detailed checks after the scorecard.

Return an improved prompt only when requested or when it is clearly useful. Keep diagnosis and rewriting distinct: do not claim the rewrite performs better without runtime evidence.

Write the report in the user's language unless the user requests another language.

## Few-shot rules

Detect examples by meaning, not only by headings. Count paired demonstrations such as input/output records, conversations, classification cases, and structured examples.

Do not automatically penalize zero-shot prompts. First determine example necessity:

- `Low`: straightforward transformation or open-ended generation;
- `Medium`: strict format, nuanced style, or several interacting constraints;
- `High`: ambiguous labels, boundary decisions, complex business rules, or exact schema behavior.

When necessity is high and no useful demonstration exists, recommend one representative example plus one boundary or failure example. An incorrect or contradictory example is more harmful than no example.

## Model compatibility rules

Read `references/model-compatibility.md` when a target model or comparison is requested.

Use verified, current model documentation supplied by the user or available through approved sources when precise capability claims matter. Otherwise:

- use capability requirements rather than folklore about vendor behavior;
- mark uncertain or time-sensitive facts as unknown;
- do not infer that a model supports a context size, modality, schema mode, tool protocol, or message role;
- do not claim one model will score higher without actual runs.

Cross-model output is a portability risk matrix, not a runtime leaderboard.

## Static versus dynamic evaluation

This version performs static evaluation. It may recommend a future dynamic plan, but must not execute external model calls by default.

When dynamic testing would materially improve confidence, propose:

- representative test cases rather than only repeating one input;
- repeat count appropriate to variance;
- fixed model/version and decoding parameters;
- deterministic validators for schemas and constraints;
- reference answers or trusted sources for accuracy and hallucination claims;
- cost and stop limits.

Always display dynamic metrics as `Not run` in a static report.

## Quality bar

A trustworthy benchmark:

- adapts criteria to the task;
- distinguishes facts, assumptions, and predictions;
- cites prompt evidence for deductions;
- explains weight changes and `N/A` decisions;
- prioritizes a small number of consequential fixes;
- avoids fake precision;
- remains useful even when no target model is specified.
