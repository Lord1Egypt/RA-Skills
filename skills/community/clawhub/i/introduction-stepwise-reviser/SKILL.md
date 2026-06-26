---
name: introduction-stepwise-reviser
description: "Revise English research paper Introduction sections with a p2-derived, step-by-step checklist: establish significance, synthesize previous/current research, articulate the gap/problem/opportunity, state the present work, and save two Markdown files. Use when the user asks to polish, rewrite, check, or improve full English Introduction paragraphs while preserving every step's revised draft, reasons, and rich examples."
---

# Introduction Stepwise Reviser

## Overview

Use this skill to revise the complete English text of a research-paper Introduction through a documented sequence of checks derived from `p2.txt`: significance, previous/current research, gap/problem/opportunity, and the present work. Preserve the paper's meaning, citations, claims, paragraph order, and discipline-specific terminology while improving rhetorical clarity and academic phrasing.

Before revising, read `references/introduction-checklist.md`. It contains the p2-derived step checklist, phrase patterns, and example transformations.

## Required Outputs

Always save two Markdown files unless the user explicitly asks for different filenames or formats:

1. Method report: if the input has a filename, save `<stem>-introduction-method.md`; otherwise save `introduction-revision-method.md`.
2. Complete revised document: if the input has a filename, save `<stem>-introduction-revised.md`; otherwise save `introduction-revised-document.md`.

Save outputs beside the input file when the Introduction comes from a file. If the Introduction comes from the prompt, save outputs in the current working directory.

## Workflow

1. Read the full Introduction text from the user's message or file. If no Introduction text is available, ask for it.
2. Preserve structural units: title or heading, paragraph breaks, citations, tables, numbered claims, abbreviations, formulas, quotations, and reference markers.
3. Build a rhetorical map of the original Introduction before rewriting: context/significance, prior research, gap/problem/opportunity, present work, and any organization sentence.
4. Apply the checklist in `references/introduction-checklist.md` one step at a time. At each step, revise the entire Introduction draft as it stands after the previous step, but only make edits justified by the current step.
5. After every step, record the step result and reasons in the method report. Include the full draft after that step, not just isolated snippets, unless the Introduction is extremely long; in that case, include every changed paragraph and clearly mark unchanged paragraphs.
6. Include rich examples for every step in the method report. Prefer examples adapted to the user's topic when possible; otherwise use general research-writing examples. Label examples as examples, not as claims about the user's study.
7. After the final step, run a consistency pass comparing the original Introduction with the revised Introduction for meaning, evidence strength, tense, modality, citations, numbers, terminology, and paragraph order.
8. Write the complete revised document as clean prose only. Do not include the report, commentary, checklists, or examples in the revised-document file.

## Method Report Structure

Use this structure for the method report:

```markdown
# Introduction Revision Method

## Source Handling
- Input source:
- Output files:
- Preservation notes:

## Original Rhetorical Map
| Paragraph | Main function | Notes |
|---|---|---|

## Step 1: Source Preservation and Rhetorical Map
### Checks Applied
### Draft After This Step
### Modification Reasons
### Examples

## Step 2: Establish Significance
### Checks Applied
### Draft After This Step
### Modification Reasons
### Examples

## Step 3: Synthesize Previous and Current Research
### Checks Applied
### Draft After This Step
### Modification Reasons
### Examples

## Step 4: Articulate the Gap, Problem, or Research Opportunity
### Checks Applied
### Draft After This Step
### Modification Reasons
### Examples

## Step 5: State the Present Work
### Checks Applied
### Draft After This Step
### Modification Reasons
### Examples

## Step 6: Integrate Flow and Final Consistency
### Checks Applied
### Draft After This Step
### Modification Reasons
### Examples

## Final Verification
- Meaning preserved:
- Claims/citations preserved:
- Tense/modality preserved:
- Paragraph structure preserved:
- Remaining issues:
```

In `Modification Reasons`, be concrete: identify which sentence or paragraph changed, what rhetorical function improved, and why the edit follows the current step. If a step requires no substantive edit, keep the previous draft under `Draft After This Step` and explain why no change was made.

## Revision Constraints

- Do not invent research findings, citations, dates, statistics, causal claims, advantages, novelty, or methods.
- Do not strengthen certainty. Preserve modal verbs and hedging such as `may`, `might`, `could`, `suggest`, and `appears`.
- Do not turn a limitation into a stronger criticism than the source supports.
- Preserve author names, citation style, abbreviations, terminology, numbers, units, variables, and quoted text.
- Improve academic phrasing only when it clarifies the Introduction's rhetorical function or sentence-level readability.
- Prefer precise verbs for research activity and contribution. Avoid repetitive generic phrasing such as `did`, `showed`, or `found` when the actual action is more specific.
- Keep the final revised Introduction coherent as a complete section, not a collection of individually polished sentences.

## Quality Checks

Before finalizing, verify that:

- The method report contains all six steps, with a draft, reasons, and examples for each step.
- The final revised-document file contains only the revised Introduction.
- The final Introduction follows the expected progression: significance/context, previous/current research, gap/problem/opportunity, present work, and optional paper organization.
- All edits are traceable to the step checklist.
- The two Markdown files exist at the required paths.
