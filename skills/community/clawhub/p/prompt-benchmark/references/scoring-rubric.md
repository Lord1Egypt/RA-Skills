# Static Prompt Benchmark scoring rubric

## Contents

1. Scoring method
2. Default weights
3. Task profiles
4. Module criteria
5. Severity and caps
6. Confidence

## 1. Scoring method

Score each applicable criterion from 0–4:

| Score | Anchor |
|---:|---|
| 4 | Explicit, coherent, executable, and suitable for the task |
| 3 | Adequate; minor ambiguity or omission with limited impact |
| 2 | Material weakness; likely to reduce consistency or quality |
| 1 | Serious weakness; execution depends heavily on guessing |
| 0 | Missing, contradictory, invalid, or unsafe |

Calculate each module percentage from applicable criteria only:

`module score = earned points / applicable possible points × 100`

Calculate the universal score from modules 1–4. Report module 5 separately as a target-model static compatibility prediction. Report module 6 as a comparison matrix, not as another contribution to the universal score.

After removing `N/A` modules, renormalize applicable module weights so they sum to 100. Calculate:

`universal score = sum(module score × normalized module weight) / 100`

Round module and overall scores to whole numbers. Scores are decision aids, not empirical performance measurements.

## 2. Default weights

| Universal module | Weight |
|---|---:|
| General quality | 30 |
| Structure and format | 25 |
| Few-shot quality | 15 |
| Safety and robustness | 30 |

If a module is `N/A`, redistribute its weight proportionally. Few-shot may be `N/A`; safety and robustness should rarely be entirely `N/A`.

## 3. Task profiles

Adjust weights by up to 10 points and explain the change.

| Task | Emphasize | Typical example need |
|---|---|---|
| Open-ended generation | goal, audience, style, constraints | Low |
| Extraction / structured output | input boundary, schema, null/error rules | Medium |
| Classification / routing | label definitions, tie-breakers, boundary cases | High |
| Transformation / summarization | fidelity, exclusions, length, audience | Low–Medium |
| Coding / tool use | environment, interfaces, validation, failure handling | Medium |
| High-stakes advice | sources, uncertainty, escalation, safety limits | Medium–High |
| Agent workflow | authority, tool boundaries, state, stop conditions | High |

## 4. Module criteria

### Module 1 — General quality

- **Goal clarity:** task and desired outcome are unambiguous.
- **Success definition:** the result can be judged against observable criteria.
- **Context sufficiency:** necessary domain, audience, and use-case context is present.
- **Input definition:** source, shape, variables, and boundaries are identifiable.
- **Instruction specificity:** actions are concrete rather than subjective or vague.
- **Constraint coherence:** must/should/must-not rules are complete and compatible.
- **Output definition:** content, level of detail, and failure response are defined as needed.
- **Feasibility:** the request does not assume unavailable information or capabilities.
- **Efficiency:** repetition and nonfunctional role-play do not obscure the task.

### Module 2 — Structure and format

- **Information architecture:** role, context, task, constraints, input, and output are sensibly ordered.
- **Instruction hierarchy:** main task, steps, priorities, and tie-breakers are clear.
- **Conflict freedom:** rules, examples, and output requirements do not contradict.
- **Data/instruction separation:** untrusted or variable content has explicit boundaries.
- **Markup validity:** Markdown, XML, JSON, or YAML is syntactically and semantically coherent.
- **Placeholder discipline:** variables use a consistent syntax and are defined.
- **Output schema quality:** fields, types, required status, enums, nulls, and error behavior are defined when needed.
- **Machine verifiability:** strict outputs can be parsed or validated without guessing.

### Module 3 — Few-shot quality

First rate example necessity as `Low`, `Medium`, or `High`.

- **Quantity fitness:** example count matches task complexity.
- **Pair completeness:** each demonstration has sufficient input and expected output.
- **Correctness:** demonstrations follow the stated rules and parse when structured.
- **Consistency:** examples agree with one another and with the output contract.
- **Coverage:** normal, boundary, ambiguous, and failure cases are represented as needed.
- **Positive/negative balance:** contrastive cases are present when category boundaries matter.
- **Bias control:** examples do not encourage copying, label imbalance, or narrow phrasing.
- **Token efficiency:** demonstrations are representative without needless repetition.

Set this module to `N/A` when examples are unnecessary. If necessity is high and examples are absent, score quantity and coverage at 0 and mark the remaining example-quality criteria `N/A`. If examples contradict rules, apply a major finding.

### Module 4 — Safety and robustness

- **Untrusted-content handling:** external content cannot silently become instruction.
- **Authority boundaries:** the prompt does not request privilege escalation or secret disclosure.
- **Privacy:** sensitive data is minimized, protected, or rejected appropriately.
- **Content safety:** foreseeable high-risk use has suitable limits or escalation.
- **Missing-input behavior:** the model asks, abstains, or returns a defined error rather than inventing.
- **Malformed-input behavior:** empty, oversized, invalid, or off-topic input has a response path.
- **Uncertainty handling:** facts, assumptions, and unknowns are distinguished.
- **Hallucination resistance:** verification or source requirements exist where factuality matters.
- **Edge cases:** conflicts, extreme values, and unsatisfiable requirements have tie-breakers.
- **Failure recovery:** tool, schema, or data failures have retry, fallback, or stop behavior as appropriate.

### Module 5 — Target-model static compatibility

Score only against an identified model profile or explicit capability requirements:

- exact model identity and profile freshness;
- message-role compatibility;
- context and output-budget fit;
- structured-output compatibility;
- tool/function protocol compatibility;
- required modality support;
- reasoning/output-explanation compatibility;
- prompt-structure portability;
- decoding-parameter assumptions;
- environment capability fit, including search, code, and files.

If exact model data is unavailable, score only what can be supported and lower confidence. Never convert unknown capability facts into deductions.

### Module 6 — Cross-model compatibility

Compare, without folding into the universal score:

- vendor-specific syntax and lock-in;
- message and system-instruction assumptions;
- structured-output requirements;
- tool-definition and invocation requirements;
- context and output budget;
- modality requirements;
- environment/tool availability;
- model-specific changes required;
- portability risk: `Low`, `Medium`, `High`, or `Unknown`;
- evidence confidence.

## 5. Severity and caps

Classify findings:

| Severity | Meaning | Suggested primary-module deduction |
|---|---|---:|
| Critical | Unsafe, impossible, or internally contradictory in a core requirement | 20–35 |
| Major | Likely to cause frequent wrong, invalid, or inconsistent results | 10–19 |
| Moderate | Noticeable quality or maintainability impact | 4–9 |
| Minor | Local polish issue with limited behavioral impact | 1–3 |

Use deductions only as calibration; derive final scores from criteria. Apply these caps:

- unresolved critical finding: affected module cannot exceed 49;
- unresolved major conflict in a core output contract: Structure and format cannot exceed 69;
- high example necessity with zero examples: Few-shot cannot exceed 49;
- exact target model unknown: target-model confidence cannot be `High`;
- no runtime evidence: do not score actual accuracy, hallucination rate, latency, cost, or consistency.

Do not deduct the same root cause twice. For example, invalid JSON belongs primarily to Structure and format; mention its robustness impact without a second full deduction.

## 6. Confidence

- **High:** prompt and evaluation context are complete; claims rely on observable text or verified model capabilities.
- **Medium:** some context or precise model details are missing, but the principal assessment is supported.
- **Low:** task intent, inputs, success criteria, or model capabilities are substantially unknown.
