---
name: introduction-language-flow-reviser
description: "Revise complete English research-paper Introduction sections using a p3-derived language-and-writing checklist for verb tense choices, sentence linkage, transition signals, passive/active choices, and paragraphing. Use when the user asks to polish, rewrite, check, or improve Introduction paragraphs step by step while preserving each step's revised draft, reasons, and rich examples, and saving two Markdown outputs."
---

# Introduction Language Flow Reviser

## Overview

Use this skill to revise the full English text of a research-paper Introduction through the language and writing-skills checks derived from `p3.txt`: verb tense choices, sentence-to-sentence linkage, transition signals, passive/active choices, and paragraphing. Preserve the original research content, citations, claims, paragraph sequence when possible, and discipline-specific terminology while improving readability, flow, tense accuracy, and communicative precision.

Before revising, read `references/language-flow-checklist.md`. It contains the p3-derived checklist, decision rules, signal categories, paragraphing guidance, and example transformations.

## Required Outputs

Always save two Markdown files unless the user explicitly asks for different filenames or formats:

1. Method report: if the input has a filename, save `<stem>-language-flow-method.md`; otherwise save `introduction-language-flow-method.md`.
2. Complete revised document: if the input has a filename, save `<stem>-language-flow-revised.md`; otherwise save `introduction-language-flow-revised.md`.

Save outputs beside the input file when the Introduction comes from a file. If the Introduction comes from the prompt, save outputs in the current working directory.

## Workflow

1. Read the complete Introduction text from the user's message or file. If no Introduction text is available, ask for it.
2. Preserve structural units: title or heading, paragraph breaks, citations, author names, numbers, units, abbreviations, formulas, quotations, reference markers, and named methods.
3. Create a diagnostic map of the original Introduction: paragraph function, key claims, current tense patterns, linkage problems, voice choices, and paragraph-length or topic-focus issues.
4. Apply the checklist in `references/language-flow-checklist.md` one step at a time. At each step, revise the full draft produced by the previous step, but make only edits justified by the current step.
5. After every step, record the step result and reasons in the method report. Include the full draft after that step, not only isolated sentence examples, unless the Introduction is extremely long; in that case, include every changed paragraph and clearly mark unchanged paragraphs.
6. Include rich examples for every step in the method report. Prefer examples adapted to the user's topic and sentence patterns when possible; otherwise use general research-writing examples. Label examples as examples, not as claims about the user's study.
7. After the final step, run a consistency pass comparing original and revised text for meaning, evidence strength, tense, modality, citations, numbers, terminology, paragraph order, and claim ownership.
8. Write the complete revised document as clean prose only. Do not include the report, checklist, examples, or commentary in the revised-document file.

## Method Report Structure

Use this structure for the method report:

```markdown
# Introduction Language Flow Revision Method

## Source Handling
- Input source:
- Output files:
- Preservation notes:

## Original Diagnostic Map
| Paragraph | Main function | Tense/flow/voice/paragraphing notes |
|---|---|---|

## Step 1: Preserve Content and Diagnose Language Flow
### Checks Applied
### Draft After This Step
### Modification Reasons
### Examples

## Step 2: Revise Verb Tense Choices
### Checks Applied
### Draft After This Step
### Modification Reasons
### Examples

## Step 3: Strengthen Sentence-to-Sentence Linkage
### Checks Applied
### Draft After This Step
### Modification Reasons
### Examples

## Step 4: Correct Transition Signals and Logical Relations
### Checks Applied
### Draft After This Step
### Modification Reasons
### Examples

## Step 5: Refine Passive/Active and Subject Choices
### Checks Applied
### Draft After This Step
### Modification Reasons
### Examples

## Step 6: Improve Paragraphing and Entry Sentences
### Checks Applied
### Draft After This Step
### Modification Reasons
### Examples

## Step 7: Integrate Final Flow and Consistency
### Checks Applied
### Draft After This Step
### Modification Reasons
### Examples

## Final Verification
- Meaning preserved:
- Claims/citations preserved:
- Tense choices justified:
- Linkage and signals coherent:
- Voice and claim ownership clear:
- Paragraph structure reader-friendly:
- Remaining issues:
```

In `Modification Reasons`, identify the paragraph or sentence changed, the language-flow problem addressed, and why the edit follows the current step. If a step requires no substantive edit, keep the previous draft under `Draft After This Step` and explain why no change was made.

## Revision Constraints

- Do not invent findings, citations, dates, statistics, methods, advantages, limitations, novelty claims, or causal relations.
- Do not change tense randomly. Treat tense as a meaning choice: past simple for study-bound findings, present simple for established facts or current paper statements, and present perfect for research trends or gaps with current relevance.
- Preserve modal strength and hedging. Do not turn `may`, `might`, `could`, `suggests`, or `appears` into stronger claims.
- Preserve citation placement unless moving a citation is necessary to keep it attached to the supported claim.
- Avoid overusing transition words. Prefer repetition linkage or clear pro-forms when they create smoother flow.
- Do not use ambiguous pronouns or pro-forms such as `this`, `these`, `it`, or `they` unless the referent is clear.
- Keep `we` and `our` referents stable. If `we` shifts from the paper's authors to the field or people generally, revise for clarity.
- Prefer non-human grammatical subjects such as `this study`, `this paper`, `the present work`, or `Section 2` when they improve ownership and style.
- Keep each paragraph focused on one main function. Split, merge, or reorder sentences only when necessary for a reader-friendly Introduction.

## Quality Checks

Before finalizing, verify that:

- The method report contains all seven steps, with a draft, reasons, and examples for each step.
- The revised-document file contains only the final revised Introduction.
- All tense changes are explained by meaning, not by grammar alone.
- Sentence links are explicit through overlap, pro-forms, semicolons, or accurate signals.
- Transition signals match their logical function: cause, result, contrast/difference, unexpectedness, addition/listing, or topic transition.
- Passive, active, and non-human subject choices are stylistically and communicatively justified.
- Paragraphs have clear entry sentences and one dominant function.
- The two Markdown files exist at the required paths.
