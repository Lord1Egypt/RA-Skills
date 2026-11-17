# Evaluation protocol

The purpose of this evaluation is to detect routing and update failures across unfamiliar domains. It is not evidence that the skill is generally effective.

## Single source of cases

[cases.json](cases.json) is the only case manifest. Do not duplicate its prompts in this document, README files, or examples.

Every case records:

- domain and severity;
- expected activation depth: none, light, or full;
- expected mode when active;
- expected judgment update for paired evidence cases.

Add a case only to cover a missing domain or mode, reproduce an observed failure, or test a genuinely ambiguous boundary. Do not add cases merely to encode the author's preferred answer.

## Review procedure

1. Run each one-turn case in a fresh conversation without naming the skill.
2. Run both turns of an evidence-update case in the same conversation.
3. Save the complete raw output before assigning labels.
4. Have a named reviewer record activation depth, selected mode, update behavior, concise evidence, and the raw-output path in JSONL.
5. Prefer a reviewer who did not write the case. If that is unavailable, disclose the conflict.
6. Score the reviewed observations:

~~~bash
python scripts/score_evals.py --results path/to/observations.jsonl --fail-on-error
~~~

[observations.example.jsonl](observations.example.jsonl) demonstrates the review schema. It is intentionally incomplete and is not a passing result set.

## Report separately

Never collapse these into one accuracy or activation number:

- false-positive activation;
- false negative;
- activation-depth mismatch;
- mode mismatch;
- evidence-update error;
- missing case;
- cases with errors by severity.

The scorer validates accounting and coverage. It cannot infer reasoning quality from wording, prove internal causality, or replace independent review.

## Baseline policy

A committed baseline must include the case-manifest revision, model and settings, raw outputs, reviewer identity or disclosed role, structured observations, and limitations.

The earlier seven-case smoke run was removed because it reused project-specific examples, lacked mode scoring and raw outputs, and was not independently reviewable. This version has no valid behavioral baseline yet.
