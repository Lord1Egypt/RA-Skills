---
name: paper-deep-reader
slug: paper-deep-reader
version: 2.1.0
description: Very helpful in deep-reading one selected research paper, journal article, arXiv paper, working paper, technical report, benchmark paper, dataset paper, replication study, or synthesis paper and producing a rigorous markdown reading note, technical summary, critique, or implementation memo. Always use when the task requires reconstructing equations, notation, derivations, theorems, estimators, algorithms, empirical identification, experiments, benchmark design, dataset construction, figures, tables, appendix evidence, assumptions, limitations, or literature context across fields such as machine learning, statistics, physics, economics, quantitative finance, systems, and related technical disciplines. Not for shallow abstract rewrites or broad multi-paper surveys unless the selected paper itself is a survey or synthesis.
metadata:
  openclaw:
    emoji: "🔎"
---

# Paper Deep Reader

Use this skill to read **one selected paper deeply** each time and turn it into a **durable, evidence-based note**.

This skill is for **serious paper reading**, not for rewriting the abstract in cleaner prose.

## First load

Before drafting, read these core references:

- `{baseDir}/routing-rules.md`
- `{baseDir}/paper-taxonomy.md`
- `{baseDir}/references/reading-workflow.md`
- `{baseDir}/references/note-template-base.md`
- `{baseDir}/references/output-contract.md`
- `{baseDir}/references/checklists/general.md`

Then route the paper and load:

- exactly **one primary adapter**
- **one to three evidence checklist packs**
- an optional **secondary adapter** only when a second contribution is independently load-bearing
- an optional **domain overlay** only if one exists in the repository and materially improves faithfulness

### Adapters currently in use

- `{baseDir}/references/adapters/theory-math-stats.md`
- `{baseDir}/references/adapters/method-algorithm.md`
- `{baseDir}/references/adapters/benchmark-evaluation.md`
- `{baseDir}/references/adapters/dataset-resource.md`
- `{baseDir}/references/adapters/empirical-econ.md`
- `{baseDir}/references/adapters/systems.md`
- `{baseDir}/references/adapters/survey-synthesis.md`
- `{baseDir}/references/adapters/replication-negative-result.md`
- `{baseDir}/references/adapters/physics.md`
- `{baseDir}/references/adapters/quant-finance.md`

### Evidence checklist packs currently in use

- `{baseDir}/references/checklists/general.md`  
  Always run this first.
- `{baseDir}/references/checklists/theory-math-stats.md`
- `{baseDir}/references/checklists/proof-rigor.md`
- `{baseDir}/references/checklists/experimental-eval.md`
- `{baseDir}/references/checklists/ablation-and-mechanism-isolation.md`
- `{baseDir}/references/checklists/robustness-and-ood.md`
- `{baseDir}/references/checklists/benchmark-fairness-and-contamination.md`
- `{baseDir}/references/checklists/reproducibility-and-compute.md`
- `{baseDir}/references/checklists/empirical.md`
- `{baseDir}/references/checklists/systems.md`
- `{baseDir}/references/checklists/physics.md`
- `{baseDir}/references/checklists/quant.md`

## Primary objective

Produce a note that lets a strong graduate student answer all of the following without reopening the paper:

1. What problem does the paper study?
2. Why does that problem matter?
3. What is the paper's main move?
4. How does the technical mechanism, argument, benchmark, dataset, or system work step by step?
5. What assumptions, approximations, identification logic, workload assumptions, or construction choices are doing the real work?
6. What evidence actually supports the main claims?
7. What is genuinely strong, weak, narrow, reusable, or fragile about the paper?

## Non-goals

Do **not** use this skill for:

- shallow abstract rewrites
- vague praise or hype language
- multi-paper literature reviews unless the selected paper itself is a survey or synthesis
- papers you have not actually read beyond title and abstract

## Operating principle

Treat paper reading as **reconstruction plus judgment**.

Your job is not only to say what the authors claim. Your job is to reconstruct the paper's intellectual structure, route it faithfully, trace claims to evidence, and record where a careful reader should trust, doubt, reuse, or extend the work.

## Required execution protocol

Follow this sequence.

### 1. Build a paper map before prose

Before writing the note, identify:

- research question
- problem setting
- main move
- key technical objects
- main claim(s)
- evidence backbone
- where the paper's intellectual load actually lives
- the primary failure risk if the paper is weaker than advertised

Write a short internal map in this form:

> The paper studies __ in the setting __. Its main move is __. It claims __, supported mainly by __. The key technical objects are __. The real intellectual load sits in __. The main failure risk is __.

If you cannot write this map, keep reading before drafting.

### 2. Route the paper before analyzing it

Use the routing rules in `{baseDir}/routing-rules.md`.

Create an internal route record in this form:

```markdown
Primary adapter:
Secondary adapter:
Evidence packs:
Domain overlay:
Route confidence:
Why this route:
```

Routing principles:

- choose exactly **one** primary adapter
- add a secondary adapter only if a second contribution is independently central
- choose **one to three** evidence packs that are most likely to change the final verdict if the evidence is weak
- use a domain overlay only when the field has recurring objects, overclaims, or traps that deserve active reminders
- prefer the **simplest faithful route**

Do **not** route only by title words or surface buzzwords. Route by the paper's real intellectual load.

### 3. Read in passes

Do not read linearly from top to bottom unless the paper is unusually simple.

#### Pass A: framing

Read title, abstract, introduction, conclusion, and figure or table captions.
Goal: identify what the authors want the reader to believe and what kind of contribution they think they are making.

#### Pass B: technical core

Read the model, method, theory, derivation, benchmark construction, dataset section, or system design sections carefully.
Reconstruct the main equations, estimators, algorithms, proof ideas, task definitions, sampling logic, or tradeoffs.

#### Pass C: evidence

Read experiments, empirics, case studies, benchmarks, robustness checks, appendix evidence, or construction validation that bears on the main claims.

#### Pass D: limits and context

Read limitations, related work selectively, and appendix sections needed to judge the claims fairly.

Do **not** stop at the main body if a central claim is only supported in the appendix or supplement.

### 4. Use the scripts to reduce drift

If the scripts in `{baseDir}/scripts/` are available, use them as a structured drafting aid. Before using any script, read its documentation `{baseDir}/scripts/README.md` and understand what it does and does not do.

Recommended order:

1. `scaffold_note.py`
2. `build_paper_map.py`
3. route the paper manually using `{baseDir}/routing-rules.md`
4. `build_notation_table.py`
5. `build_claim_matrix.py`
6. `build_limitation_ledger.py`
7. `render_final_note.py`

Use the scripts to create first drafts of the note scaffold and internal artifacts. Then review and correct them against the paper. The scripts are helpers, not authorities.

### 5. Prefer scripted artifacts when the note will be saved

When the user wants a saved markdown note, prefer this flow:

- scaffold the note from `{baseDir}/references/note-template-base.md`
- draft the paper map
- route the paper explicitly
- draft the notation table when notation is nontrivial
- draft the claim-evidence matrix for the main claims
- draft the limitation ledger
- render the final note and then revise it manually for accuracy and pedagogy

If the note is short and purely conversational, you may skip the scripts, but you must still follow the same intellectual protocol.

## Mandatory internal outputs

Before finalizing the note, build these internal structures. They can remain implicit unless the user asks for them, but the final note must reflect them.

### A. Paper map

A compact statement of problem, setting, contribution, evidence backbone, and main failure risk.

### B. Route record

A compact routing decision with:

- primary adapter
- optional secondary adapter
- one to three evidence packs
- optional domain overlay
- route confidence
- short justification

### C. Notation table

When notation is nontrivial, record:

- symbol
- meaning
- type / shape / domain
- units if relevant
- where it first matters

### D. Claim-evidence matrix

For each major claim, record:

- the claim itself
- whether it is the authors' stated claim or your inference
- what evidence supports it
- where that evidence appears
- how strong the support is
- any caveat or missing check

### E. Limitation ledger

Separate:

- limitations explicitly acknowledged by the paper
- limitations you infer as a careful reader

## Core rules

1. **Read before judging.** Never infer the entire contribution from title and abstract alone.
2. **Separate authors' claims from your evaluation.** Mark the distinction clearly.
3. **Preserve the mathematical or technical spine.** Keep the note anchored in equations, estimators, theorem statements, algorithms, benchmark construction, data construction, identification logic, or system tradeoffs when relevant.
4. **Trace claims to evidence.** Strong statements require concrete support from sections, figures, tables, appendices, proofs, or benchmarks.
5. **Explain mechanisms, not just outcomes.** Answer why the method, argument, benchmark, dataset design, or system should work and when it should fail.
6. **Prefer exactness over praise.** Replace words like “powerful,” “novel,” or “impressive” with concrete statements.
7. **Do not hide uncertainty.** If the paper is unclear, underspecified, overstated, or weakly evidenced, say so directly.
8. **Use scripts as drafts, not verdicts.** Heuristic extraction must always be checked against the paper.
9. **Choose the simplest faithful route.** More adapters or packs do not automatically make a better note.

## Adapter and checklist rule

Always keep the common structure from the base template, then expand or tighten sections using the routed adapter and chosen evidence packs.

- Use one adapter for a clean single-contribution paper.
- Use two adapters only when the paper is genuinely mixed and the second contribution is independently load-bearing.
- Do not bolt on irrelevant sections just to satisfy a template.
- Run `general.md` first, then the chosen evidence packs, then any adapter-specific or domain-specific checks.

## Writing contract for the final note

Follow the output contract in `{baseDir}/references/output-contract.md`. Use the base note template as the default scaffold, then adapt it to the routed paper type and evidence profile.

## Evidence rule

For every important conclusion in the note, ask:

1. Is this the authors' claim, or my inference?
2. What concrete evidence supports it?
3. How strong is that support?
4. What would make me trust it less?
5. Did I record that caveat in the note?

If you cannot answer these questions, keep reading or weaken the statement.
