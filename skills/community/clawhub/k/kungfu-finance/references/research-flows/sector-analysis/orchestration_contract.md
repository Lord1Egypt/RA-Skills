# Sector Analysis Orchestration Contract

Source of migration:

- `/Users/jc34/.codex/skills/sector-analysis/SKILL.md`

This file records the orchestration-level contract that was previously only implicit in the original `sector-analysis` `SKILL.md`.
It is now part of the repo-controlled truth for `kungfu_finance`.

## Architecture

The sector deep-research methodology uses a strict `主编排器 + 步骤模块` architecture:

- orchestration root: `SKILL.md`
- prompt-layer assets:
  - `orchestrator_system.md`
  - `worker_system.md`
  - `synthesizer_notes.md`
- ordered step modules:
  - `step-0-macro`
  - `step-1-filter`
  - `step-2-classify`
  - `step-3-mining`
  - `step-4-thesis`
  - `step-5-position`
  - `step-6-risk`
  - `step-7a-skeptic`
  - `step-7b-advocate`
  - `step-8-verdict`
  - `step-9-output`

The debate steps are mandatory here as well.

## Execution Protocol

Each step must follow the same orchestration discipline:

1. read the current step module
2. execute pre-conclusion dialectic before fixing the step conclusion
3. gather evidence and update the shared context
4. pass gate checks before entering the next step
5. if later evidence invalidates earlier reasoning, trigger the discovery-correction protocol

Gate outcomes:

- `✅ 通过`: continue
- `⚠️ 部分通过`: continue with lower confidence
- `❌ 未通过`: block or downgrade
- `🔄 发现矛盾`: revise upstream context before continuing

## Pre-Conclusion Dialectic

Every step must perform the same three-part dialectic:

1. identify the assumptions supporting the emerging conclusion
2. run a directed counter-search against the strongest assumption
3. adjudicate:
   - `✅ 假设稳固`: conclusion stands
   - `⚠️ 假设受挑战`: conclusion stands with reduced confidence
   - `❌ 假设不成立`: revise the conclusion instead of ignoring the evidence

## Discovery Correction Protocol

If a later step conflicts with an earlier conclusion:

1. record the contradiction
2. determine whether it is marginal or core
3. revise the earlier conclusion if the contradiction is core
4. propagate the revised context through dependent reasoning
5. continue the current step using corrected context

## Step Gate Summary

### Step 0

- macro regime assessed
- reflexivity and regulatory risk assessed
- if macro is `⚫`, stop analysis

### Step 1

- lifecycle classification completed
- scale / CAGR / penetration collected
- if the sector is `📉夕阳`, stop the cycle analysis and output a decay report

### Step 2

- concept class determined
- core indicators listed
- price-linkage search commands executed

### Step 3

- at least 2 iterative search rounds completed
- information reliability reaches A or B
- key data carries timestamps
- C-level reliability can continue only with low-confidence marking

### Step 4

- core logic identified
- validity judged
- red-team review completed
- time-force analysis completed
- if red-team overturns the thesis, direction must be corrected

### Step 5

- current phase determined
- dual-cycle position completed when applicable
- next-three-month catalyst calendar and anchors defined

### Step 6

- direction baseline and final direction determined
- no exact position-size advice
- four risk categories and scenario matrix defined
- key-variable sensitivity completed

### Step 7A

- at least 3 critical or major skeptic arguments
- independent cross-check of phase positioning
- at least 1 new risk beyond prior steps

### Step 7B

- at least 3 strong advocate arguments
- new data beyond prior steps
- at least 1 underpriced upside factor

### Step 8

- every major skeptic challenge receives an explicit ruling
- phase-position stability is tested
- verdict is one of `UPHELD / MODIFIED / OVERTURNED`
- revision instructions are required for modified or overturned cases

### Step 9

- completeness checklist passes
- debate appendix is present
- SVG belongs to later parity layers and is not yet fully enforced in current preview runtime
