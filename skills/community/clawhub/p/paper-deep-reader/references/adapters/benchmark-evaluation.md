# Adapter: Benchmark / Evaluation

Use this adapter when the paper's main contribution is a benchmark, evaluation protocol, task operationalization, judge or evaluator design, or a new framework for comparing models, agents, systems, or scientific claims.

## What to prioritize

1. What capability, behavior, or failure mode the benchmark is supposed to measure.
2. Why earlier evaluation was insufficient or misleading.
3. Task construction, metric definition, and evaluator design.
4. Contamination, leakage, or gaming risks.
5. Slice-wise behavior, failure cases, and coverage of the benchmark.
6. Whether the benchmark creates a better measurement instrument rather than only a harder leaderboard.

## Questions to answer in the note

- What exactly is being measured?
- Why is the proposed benchmark or evaluation protocol needed?
- What assumptions link the benchmark score to the capability the authors claim to measure?
- How are tasks, prompts, labels, rubrics, or judges constructed?
- Are the baselines and evaluation budgets fair?
- Could a model score well for the wrong reasons?
- What does a high score fail to tell us?

## Minimum insertions into the note

Add or expand these sections:

### Problem setup

- target capability or behavior being evaluated
- evaluation regime and intended use case
- what earlier benchmarks or metrics miss

### Technical core

- benchmark construction logic
- task categories or slices
- metric definition
- evaluator or judge pipeline
- any formal scoring rule or aggregation scheme

### Evidence

- baseline systems or models being compared
- benchmark coverage and task diversity
- contamination or leakage checks
- slice-wise results and failure cases
- comparison between old and new evaluation protocols when available

### Limitations and failure modes

Include discussion of:

- metric validity limits
- benchmark narrowness
- judge bias or rubric fragility
- whether the benchmark can be gamed or overfit

## Special reading rules

- Separate “harder benchmark” from “better benchmark.”
- Ask whether the benchmark measures the claimed capability or merely correlates with it.
- Read appendices carefully when scoring instructions, data filtering, or contamination checks are moved out of the main text.
- Look for hidden asymmetries in prompt budget, tool access, decoding setup, or evaluator privileges.
- Treat benchmark design choices as technical mechanisms, not as administrative details.

## Typical failure patterns to watch for

- metric that does not track the claimed capability well
- benchmark tasks too narrow to support broad conclusions
- contamination checks that are weak or absent
- baseline settings that are not apples-to-apples
- hidden tuning against the benchmark itself
- aggregate score hiding severe slice failures
- judge or evaluator pipeline that introduces bias or instability

## Reusable note prompts

- “The benchmark is trying to operationalize … by measuring …”
- “This evaluation is more informative than prior work because …”
- “A high score here should be interpreted as … rather than …”
- “The main validity risk is …”
- “The benchmark is broad in … but narrow in …”
