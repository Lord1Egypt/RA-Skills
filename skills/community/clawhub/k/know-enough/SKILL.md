---
name: know-enough
description: >
  Part of the Overpowered skill suite.
  Acquire the minimum sufficient knowledge needed to make the next material decision: identify knowledge gaps, choose the right authoritative or contextual sources, retrieve selectively, assess sufficiency, and stop when more retrieval is unlikely to change the outcome. Use when organization-specific, historical, current, or otherwise missing knowledge could materially affect the task and retrieval/RAG/search tools are available.
compatibility: >
  Works with any Agent Skills-compatible harness. Requests functional acquisition capabilities and uses only sources and means actually available; specialized classification is optional.
metadata:
  suite: overpowered
  suite_url: https://github.com/raguets/overpowered
  level: "1-knowledge"
  version: "0.1.0"
---

# Overpowered / Know Enough

## Core rule

**Know enough to act well — no less, no more. Retrieval must have an information objective.**

Before each search, be able to complete:

> I am looking for **[information]** because it could change **[decision/action]**.

If you cannot complete that sentence, do not retrieve yet.

## Procedure

1. **Define the next decision.** What are you trying to decide, produce, or verify now?
2. **Inventory current knowledge.** Separate known facts, assumptions, and material unknowns.
3. **Prioritize gaps.** Retrieve only gaps that can materially change the next decision. If existing evidence suffices, do not search.
4. **Choose the source by role.** Prefer an available knowledge-source registry. Distinguish:
   - authoritative / normative;
   - precedent / historical;
   - observational / operational;
   - reference / explanatory.
5. **Plan minimal acquisition.** Check source access and available functional capabilities, then choose the simplest sufficient strategy using `references/adaptive-retrieval.md`. Search for the missing fact or evidence, not the whole topic; the harness selects existing means and executes the plan.
6. **Evaluate results.** Check relevance, authority, freshness, scope, coverage, and contradictions. Preserve source identifiers, passages, and citations; distinguish no result, inaccessible source, conflicting evidence, and insufficient evidence.
7. **Iterate only if needed.** Take one targeted step to close a material gap or resolve a conflict, using available reconciliation support when appropriate.
8. **Stop when sufficient.** Judge sufficiency against the task and risk. Additional retrieval should be unlikely to change the next decision; if available means cannot close a material gap, report the limit instead of looping or inventing evidence.

## Adaptive retrieval

Read `references/adaptive-retrieval.md` when a material gap requires choosing an acquisition strategy. It covers direct, structured, lexical, semantic/hybrid, relational, preparation, and optional classification capabilities without prescribing implementations.

For a non-trivial plan, briefly state: **knowledge objective → desired capability/capabilities → accessible sources → expected evidence → stopping criterion**. Use ordinary language, not a required machine schema. Prefer rules or the active model's reasoning for simple choices; specialized classification is never required. Combine capabilities only when the question and results justify it.

## Retrieval budget

Default to the smallest useful search sequence. Expand only when:

- first results are ambiguous or weak;
- a material conflict appears;
- coverage is insufficient for the decision;
- a different evidence role is required, such as current policy plus precedent.

## Output contract

Keep a compact knowledge state when the task is non-trivial:

```text
Decision to support
Known
Missing but material
Sources consulted + role
What was learned
Remaining uncertainty
Sufficiency: ENOUGH / NOT ENOUGH
```

If `NOT ENOUGH`, say exactly what is missing and whether progress can safely continue.

## Knowledge-source registry

Read `references/knowledge-source-registry.md` when multiple knowledge bases or retrieval tools exist.
Use `references/knowledge-sources.example.yaml` as a portable example.

## Gotchas

- Do not retrieve everything because retrieval is available.
- Do not ask the user for a fact that an available source can cheaply establish.
- Do not treat semantic similarity as authority.
- Do not treat precedent as current policy.
- Do not keep researching after the decision is already robust to additional information.
- If the task is purely transformative and all required content is present, do not retrieve.

## Composition

These are possible companions when available; the harness or orchestration layer selects installed means, not this knowledge policy.

- Need historical analogs → `find-precedent`.
- Sources materially disagree → `reconcile`.
- Needed facts live in structured files → `ask-the-data`.
- Material claim must be supported → `evidence-first`.

## Stop condition

Stop when the next material decision can be made with explicit uncertainty and more retrieval is unlikely to change it.
