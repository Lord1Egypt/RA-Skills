---
name: multi-council-decision-engine
description: Give your agent a virtual board of 8 specialized reasoning frameworks (strategy, risk, market, operations, ethics, forecasting, execution, AI-engineering) that independently evaluate a decision and synthesize a go/hold/kill verdict with confidence and concrete findings.
version: 1.0.0
metadata:
  openclaw:
    requires:
      env:
        - OPENROUTER_API_KEY
      bins:
        - python3
    primaryEnv: OPENROUTER_API_KEY
---

# Multi-Council Decision Engine

Most agents either skip strategic evaluation entirely or bolt on a single
"is this a good idea?" LLM call. This skill gives your agent 8 distinct
reasoning-framework "councils" — each one applies a genuinely different
analytical lens (inversion/mental-models for strategy, antifragility/black-swan
for risk, capital-allocation/reflexivity for market, workflow/bottleneck for
operations, stakeholder/compliance for ethics, probabilistic/scenario for
forecasting, first-principles for execution, architecture-tradeoffs for AI
engineering) — then mechanically synthesizes their votes into one verdict.

This is not "ask the AI for advice" — it's a structured, repeatable decision
gate: each council returns the same JSON shape (summary, key findings, risks,
recommendation, confidence), risk/ethics councils get hard veto power over
"kill" votes, and the synthesis is computed by counting votes, not by asking
a model to summarize itself.

## Why this matters

A single LLM call asked "should I do X?" tends to be agreeable and shallow.
Running the same question through 8 independently-prompted, methodologically
distinct frameworks and forcing them into a structured verdict catches things
a single pass misses — this was built and battle-tested gating real business
decisions (which is also exactly how a bug was caught during validation: see
the synthesis-shape note below).

## Setup

1. Copy both files (`business_mind_tree.py`, `venture_council_gate.py`) into
   your project — they're designed to work together but `business_mind_tree.py`
   can be used standalone if you only need raw council calls without the
   gate/verdict wrapper.
2. Set `OPENROUTER_API_KEY` in your environment.
3. Call a single council directly, or run the full gate:

   ```python
   from business_mind_tree import strategy_council, multi_council

   # one council
   result = strategy_council("Should we raise prices 10% this quarter?")
   print(result["recommendation"], result["confidence"])

   # multiple councils + synthesis
   result = multi_council(
       "Should we raise prices 10% this quarter?",
       councils=["strategy", "risk", "market"],
   )
   print(result["synthesis"]["consensus_recommendation"])
   ```

   Or use the higher-level gate (runs all 8 councils, returns a clean verdict):

   ```python
   from venture_council_gate import run_venture_gate

   gate = run_venture_gate("New venture idea: ...", venture_key="my_venture")
   print(gate.verdict, gate.confidence, gate.synthesis)
   ```

## Important: synthesis is a STRING, not a dict

`multi_council()`'s raw return has `result["synthesis"]` as a *dict*
(`consensus_recommendation`, `all_findings`, `all_concerns`, etc). The gate
functions in `venture_council_gate.py` already convert this to readable text
via `_synthesis_to_text()` before returning it on `GateResult.synthesis` —
if you build your own wrapper around `multi_council()` directly, don't
assume `result["synthesis"]` is already a string, or you'll hit a `TypeError`
the first time you try to slice or concatenate it. This was a real bug found
in production use before this skill was published — `_synthesis_to_text()`
is the fix, kept in to save you from rediscovering it.

## Models used

Most councils run on a dynamically-selected "heavy" model (compares current
flagship candidates by price/context-window and picks the cheapest in the
top tier — currently checks `gpt-5.5`, `claude-opus-4.8`, `glm-5.2`). Light
councils (operations, execution) use a cheaper fixed model. Override
`COUNCILS` in `business_mind_tree.py` if you want different model choices.

## Cost

Each council call costs roughly $0.001-$0.01 depending on prompt length and
model selected (logged to `cost_log.json` next to the script). A full 8-council
gate run costs roughly $0.02-$0.08 total.
