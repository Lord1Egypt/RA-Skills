---
name: illustrated-paper-guide
description: |
  Create or improve a source-grounded study guide for an academic paper or PDF. Use for new-paper intake, competing top-down reading plans, big-picture explanations, phased reading checkpoints, figure or panel walkthroughs, coverage audits, limitations, explanatory diagrams, or follow-up answers written back into durable notes. Trigger phrases include "read this paper", "paper study guide", "compare reading plans", "explain this figure", "turn this PDF into notes", and "make a reading checklist".
license: MIT-0
metadata:
  companion-skill: teaching-diagram-maker
---

# Illustrated Paper Guide

Turn a paper into a durable learning artifact that helps a reader understand,
resume, verify, and question the work. The output is a study guide, not a
replacement for the paper.

## Companion Skill

This repository bundles `teaching-diagram-maker`.

- This skill owns the guide structure, evidence reading, checkpoints, and the
  decision about when and where a diagram is useful.
- `teaching-diagram-maker` owns diagram construction, editable SVG craft, and
  rendered visual QA.

When a custom diagram is needed, invoke `teaching-diagram-maker`. If the host
cannot invoke companion skills, follow its bundled `SKILL.md` directly before
creating the diagram.

## Core Rules

- Match the user's requested language. If none is specified, match the existing
  notes. Preserve paper titles, model names, dataset names, and quotations in
  their original language.
- Introduce technical terms with their English form on first use when useful.
- Explain in the order: why it matters, where it is used, then how it works.
- Distinguish what the paper directly supports from your interpretation and
  from open questions. Never invent citations, measurements, or mechanisms.
- Start with the whole-paper view. Details should deepen the overview, not
  reveal the main conclusion for the first time.
- Optimize time to first useful understanding. Give the reader a correct,
  low-resolution mental model early; increase resolution in later passes.
- Speed comes from reordering, not silent omission. Inventory the source once,
  and give every inventoried coverage unit an explicit read-now, read-later,
  or out-of-scope disposition.
- Settle and review the shallow-to-deep reading route before generating its
  checklist. The checklist records the final route; it does not design it.
- When the user asks a conceptual follow-up, answer in chat and write the
  reusable explanation into the relevant body section unless they opt out.
- Do not collect every follow-up in a detached FAQ. Put it beside the concept,
  result, or figure it clarifies.
- When reuse rights and repository policy allow it, embed a readable local copy
  of each core paper figure beside its explanation. Do not make the learner
  switch to the PDF merely to see evidence the guide is actively discussing.
  Keep the canonical paper link for attribution and surrounding context.

## Choose the Workflow

### New guide

1. Locate and inspect the paper, existing notes, and repository instructions.
2. Establish the canonical version, paper type, reader goal, available time,
   bibliographic facts, and central claim from the source. Use reasonable
   defaults instead of blocking on optional preferences.
3. Inventory sections, figures, tables, central equations, appendices or
   supplements, major claims, assumptions, and limitations. This source
   inventory is shared by all route proposals.
4. Read `references/reading-path-competition.md`. Choose the reader budget,
   generate genuinely different candidate routes, compare them with the fixed
   rubric, and synthesize one progressive route. Route agents propose only;
   the main agent is the single writer.
5. Read `references/paper-guide-template.md` and draft the guide from the
   merged route, from fast orientation to full coverage.
6. Read `references/figure-reading-rubric.md` before extracting or explaining
   figures. Add teaching diagrams where structure, comparison, timing, space,
   or causal sequence is hard to understand.
7. Have a non-author reader audit the source, inventory, coverage ledger,
   merged route, and draft guide whenever multiple readers were used. Resolve
   blocking findings and freeze the guide headings.
8. Generate the checklist in the same
   top-down order. Keep source coverage in `COVERAGE.md` or a compact coverage
   table; do not turn the learner checklist into a copy of the source TOC.
9. Mechanically validate checklist links and completion criteria, then validate
   claims, figures, limitations, and coverage.

### Improve an existing guide

1. Read the guide and its checklist before editing.
2. Find the weakest learning checkpoint or the section named by the user.
3. Patch that section in place, preserving the existing voice and structure.
4. Update the checklist and stable anchor if the heading changes.
5. Verify every changed image and link.

### Answer a follow-up question

1. Identify the body section where the concept first matters.
2. Give a direct answer in chat.
3. Add a concise explanation, table, example, or teaching diagram to that same
   section.
4. Keep historical FAQ sections as appendices; migrate useful content into the
   main narrative when touching that topic.

Follow-up questions, one-figure explanations, and focused edits stay
single-reader. Do not restart route competition for an already established
guide unless the user's goal or the paper interpretation has materially
changed.

## Reader Budget and Review Gate

For a new full guide, use parallel readers only when they improve the route:

- **Zero subagents:** focused follow-up, single figure, or local guide repair.
- **One subagent:** short, linear paper with a clear contribution; the main
  agent creates the mechanical inventory while the subagent enriches the
  claim-to-evidence mapping.
- **Two subagents by default:** one argument-first route and one
  learner/evidence-first route. The main agent compares and merges them.
- **Two route subagents plus a dedicated reviewer:** long review or book
  chapter, dense theory or mathematics, many major visuals or supplements,
  cross-domain prerequisites, or an explicit exhaustive request. Use three
  route proposals only when the user explicitly asks for three-way comparison.

Page count is only a hint. Escalate when two or more complexity signals occur:
more than ten major figures or tables, necessary supplementary evidence,
interdependent theory and experiments, substantial cross-domain background,
multiple plausible central claims, or equation-by-equation reading needs.

For the default two-route workflow, reuse one reader after synthesis for the
independent source audit when a dedicated reviewer is not warranted. Candidate
routes may disagree about order, but not vote on facts;
the source and coverage audit decide factual and evidentiary questions. If the
host has no subagent support, run separate argument-first and evidence-first
self-passes and disclose that they were not independent.

## Required Deliverables

For a full paper guide, prefer this folder shape:

```text
README.md          # Main illustrated study guide
CHECKLIST.md       # Linked, testable reading checkpoints
COVERAGE.md        # Source inventory and audit ledger for a full new guide
images/            # User-created diagrams and permitted local crops
scripts/           # Reproducible extraction or generation scripts
paper.pdf          # Optional local input; never required in a public output
```

The guide should include:

1. A short statement that this is a guide, not the original paper.
2. A link to `CHECKLIST.md` near the top.
3. Bibliographic information with a DOI or canonical source link when known.
4. A Big Picture section containing the problem, method, main results, and
   reading navigation.
5. Deeper sections for concepts, mechanism, evidence, figures, limitations,
   takeaways, and questions worth asking.
6. A glossary for recurring abbreviations.
7. Reproduction notes for generated or cropped images.
8. A progressive reading route with explicit outputs, stop points, and
   deferred material.

For a full new guide, use `COVERAGE.md`. For a short, linear paper, a compact
coverage table in `README.md` is sufficient. The ledger serves the guide author
and reviewer; the checklist serves the learner.

For a short answer or targeted edit, create only the artifacts that support the
requested scope. Do not force a full guide onto a small task.

## Big Picture First

Before detailed terminology or figure panels, ensure the reader can answer:

- What problem or gap motivated the paper?
- What did the authors actually do?
- What are the main results and overall claim?
- What should I read next, and where may I stop for a shallow pass?

A useful full-guide sequence is:

```text
BP  Big Picture
A   Story and vocabulary
B   Short explanation and significance
C   Research question and mechanism
D   Main results
E   Original figures and panels
F   Evidence boundaries, limitations, takeaways, and author questions
```

## Figure Handling

Read `references/figure-reading-rubric.md` before working with paper figures.

Core sequence for a permitted multi-panel figure:

1. Embed the complete figure first. Use a source link alone only when reuse
   rights are unclear, the source cannot be extracted readably, or repository
   policy forbids local copies; record the reason.
2. State the question answered by the figure as a whole.
3. Split or discuss individual panels.
4. Explain the visible evidence before stating the conclusion.
5. Record reproducible crop coordinates when crops are created.

Explain axes, units, colors, legends, marks, controls, uncertainty, and the
exact region that supports the claim. Point out likely novice misreadings.
Every embedded source figure needs a nearby attribution naming the paper,
figure number, canonical source, license or permission basis, and whether the
image is a full copy or crop. Preserve panel letters, axes, units, legends,
scale bars, and other claim-bearing context. Inspect the rendered image at the
size a learner will actually read, not only the source PNG at full resolution.

Custom explanatory diagrams complement paper figures; they do not silently
replace source evidence. Invoke `teaching-diagram-maker` for their creation and
QA.

## Reading Checklist

Every long guide needs a companion `CHECKLIST.md`. Each checkpoint must:

- be a Markdown checkbox;
- link to a stable explicit anchor in `README.md`;
- use the exact same title as the target heading;
- state a falsifiable completion criterion, such as explaining a mechanism or
  identifying the evidence for a claim without looking.

Put the settled top-down reading sequence at the top, followed by detailed
checkpoints and durable reading records. Generate it only after the guide
review stabilizes headings. When reorganizing an existing checklist, preserve
checked items as history; never uncheck them or treat an old check as proof
that materially revised content has been revalidated.

## Coverage Ledger

The coverage ledger prevents speed from becoming accidental omission. Record:

- source locator and kind: claim, section, figure, table, equation, method,
  assumption, limitation, appendix, or supplement;
- importance and evidence type;
- guide anchor and reading pass;
- disposition: read now, return in L1-L4, or out of scope with a reason;
- guide state: inventoried, mapped, explained, or tested;
- review state: pending, pass, or blocker, plus unresolved uncertainty.

Keep the inventory proportional: track top-level sections, claim-bearing
subsections, decisive figures or tables, central equations, and appendices or
supplements that materially affect the conclusion. Split panels only when they
support distinct claims; group procedural or reference-only material.

Operational completeness means all central abstract or conclusion claims map
to evidence; every core figure or table is explained or explicitly deferred;
all top-level sections and materially relevant supplements have a disposition;
and assumptions or limitations that change the claim's scope are present. It
does not mean rewriting every sentence of the paper.

Ship only when central claims are mapped to evidence; decisive figures and
tables are explained now or assigned a later level; scope-changing assumptions
and limitations appear in the guide; every core or in-scope row has review
passing; deferred and out-of-scope dispositions have review passing; no review
rows remain pending or blocked; and every out-of-scope item has a reason.

Use explicit anchors because generated heading slugs vary across renderers:

```html
<a id="ckpt-d2"></a>
## D2 Main result: {descriptive title}
```

```markdown
- [ ] [D2 Main result: {descriptive title}](./README.md#ckpt-d2)
  **Done when:** I can identify the comparison and the evidence supporting it.
```

## Math and Abbreviations

- Use `$...$` for inline math and `$$...$$` for display math in Markdown.
- Do not use `\(...\)` or `\[...\]` where the renderer treats backslashes as
  escapes.
- Expand abbreviations near first use and near figures where a reader needs
  them. Do not assume field-specific shorthand is universal.

## Copyright and Privacy

- Do not add papers, publisher figures, paywalled supplements, private notes,
  or confidential conversations to a public repository unless the license or
  explicit permission allows redistribution.
- A citation or DOI does not grant redistribution rights.
- In private notes, local figure crops may be used as permitted by the user's
  context. In public outputs, embed source figures when reuse rights are clear
  and attribution requirements are met. Otherwise use source links, figure
  references, or original teaching diagrams and record why embedding was not
  permitted.
- Never expose local absolute paths, credentials, private contacts, or source
  repository names in a distributable guide.

## Verification

Before finishing:

- Confirm the Big Picture states problem, method, and conclusion.
- Confirm claims trace to the paper and interpretations are labeled.
- Confirm the guide links to `CHECKLIST.md` when the guide is long.
- Confirm checklist link labels exactly match target headings and every anchor
  exists.
- Confirm the checklist follows the reviewed reading route and was generated
  after headings stabilized.
- Confirm every source-inventory item has a disposition, and every deferred
  item has a reason and a later return point.
- Confirm each central claim maps to evidence and that methods, controls,
  negative results, assumptions, and limitations were not silently dropped.
- Confirm the independent reviewer resolved all blocking source-grounding,
  coverage, and causal-overstatement findings.
- Confirm every core figure is embedded when legally and technically
  permitted, or has a documented link-only reason.
- Confirm referenced images exist, match the cited paper version and figure,
  render at a readable size, retain claim-bearing labels and legends, include
  nearby attribution and reuse basis, and have reproduction scripts that still
  run.
- Render and inspect changed diagrams through `teaching-diagram-maker`.
- Scan for raw `\[` or `\(` math delimiters when the target renderer does not
  support them.
- Report source limitations, unreadable panels, uncertain interpretations, and
  any copyright constraint that prevented embedding an image.
