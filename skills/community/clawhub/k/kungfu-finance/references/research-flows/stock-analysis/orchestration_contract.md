# Stock Analysis Orchestration Contract

Source of migration:

- `/Users/jc34/.codex/skills/stock-analysis-v2/SKILL.md`

This file records the orchestration-level contract that was previously only implicit in the original `stock-analysis-v2` `SKILL.md`.
It is now part of the repo-controlled truth for `kungfu_finance`.

## Architecture

The stock deep-research methodology uses a strict `主编排器 + 步骤模块` architecture:

- orchestration root: `SKILL.md`
- prompt-layer assets:
  - `orchestrator_system.md`
  - `worker_system.md`
  - `synthesizer_notes.md`
- ordered step modules:
  - `step-0-macro-sector`
  - `step-1-company-profile`
  - `step-1b-forward-advantage`
  - `step-2-financials`
  - `step-3-valuation`
  - `step-4-price-action`
  - `step-5-thesis`
  - `step-6-catalyst`
  - `step-7a-skeptic`
  - `step-7b-advocate`
  - `step-8-verdict`
  - `step-9-output`

The debate steps are mandatory and cannot be omitted as optional polish.

## Execution Protocol

Each step must follow the same execution discipline:

1. read the current step module
2. execute pre-conclusion dialectic before writing the step conclusion
3. gather evidence and update the shared context
4. run gate checks before entering the next step
5. if a later discovery contradicts an earlier conclusion, trigger the discovery-correction protocol

Gate outcomes:

- `✅ 通过`: continue
- `⚠️ 部分通过`: continue with reduced confidence
- `❌ 未通过`: block or downgrade
- `🔄 发现矛盾`: correct earlier context before continuing

## Pre-Conclusion Dialectic

Every step must run the three-part dialectic before finalizing a conclusion:

1. identify the 1-2 assumptions that most strongly support the emerging conclusion
2. run a directed counter-search against the strongest assumption
3. adjudicate the assumption:
   - `✅ 假设稳固`: conclusion stands
   - `⚠️ 假设受挑战`: keep conclusion but lower confidence and mark uncertainty
   - `❌ 假设不成立`: modify the conclusion instead of ignoring the counter-evidence

## Discovery Correction Protocol

If a later step finds evidence that materially conflicts with an earlier conclusion:

1. record the contradiction in shared context
2. assess whether it is marginal or core
3. if core, revise the earlier conclusion in shared context
4. propagate that revision through dependent later reasoning
5. continue the current step using the corrected context

## Step Gate Summary

### Step 0

- macro environment rated
- industry trend and concept-development context established
- cross-sector concept scan completed
- regulatory environment assessed
- if macro is `⚫`, stop analysis

### Step 1

- business model, moat, management, life stage completed
- weak moat must be marked as risk

### Step 1B

- forward-advantage scan completed
- concept purity / maturity / migration / exclusivity assessed when triggered
- low-purity concepts must be capped conservatively

### Step 2

- at least 3 years of key finance data obtained
- 3-year forward forecast completed
- profitability / health / growth / red-flag checks completed
- serious post-exemption red flags force downgrade

### Step 3

- trading comps completed with at least 5 comps
- DCF-lite completed
- SOTP completed when triggered
- valuation range / margin of safety / sensitivity completed

### Step 4

- price data and supporting inputs collected
- trend / support-resistance / money-flow direction / chip structure / unusual movement completed

### Step 5

- thesis built with paradigm level and company role
- red-team review completed with kill-switches
- five-dimensional consistency checked
- if red-team overturns the thesis, rating must be downgraded

### Step 6

- catalyst calendar completed
- scenario matrix completed
- explicit analysis horizon declared
- no exact position size or buy-sell price advice

### Step 7A

- at least 3 critical or major skeptic arguments
- each argument backed by evidence
- at least 1 new risk not already surfaced upstream

### Step 7B

- at least 3 strong advocate arguments
- arguments contain new positive evidence, not just repetition
- at least 1 new upside factor not previously surfaced

### Step 8

- every major skeptic challenge receives an explicit ruling
- strongest skeptic and advocate arguments are directly confronted
- verdict is one of `UPHELD / MODIFIED / OVERTURNED`
- if modified or overturned, concrete revision instructions are mandatory

### Step 9

- completeness checklist passes
- report keeps `[事实]` / `[推演]` separation
- debate appendix is present
- SVG / quality-gate belong to later parity layers and are not yet fully enforced in current preview runtime
