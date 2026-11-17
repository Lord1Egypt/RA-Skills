# Figure Reading and Reuse Rubric

Use this rubric for original paper figures, screenshots, and extracted panels.

## Before Interpretation

1. Confirm the figure number and caption.
2. Read the relevant Results and Methods text.
3. Identify the comparison, unit of analysis, sample size, and uncertainty
   display when available.
4. Determine whether the image may be embedded in the intended output.

If reuse rights are unclear, do not add the figure to a public repository.
Link to the source and describe the panel instead, or create an original
teaching diagram that does not copy the publisher's artwork.

If reuse rights and repository policy permit local copying, embed the source
figure beside the explanation. A link remains useful for the caption and paper
context, but it should not force the learner to context-switch merely to see
the evidence being discussed.

## Full Figure Before Panels

For a permitted multi-panel figure:

1. Present the complete figure first. Fall back to a source link only when
   embedding is not legally or technically permitted, and state the reason.
2. Explain what question the entire figure addresses.
3. Explain how the panels form one argument.
4. Then inspect individual panels.

This prevents local panel details from being mistaken for the paper's whole
claim.

## Panel Explanation

For each important panel, cover:

- **What is shown?** Experimental condition, model output, anatomy, or data.
- **How do I read it?** Axes, units, color scale, symbols, lines, boxes, labels,
  controls, and uncertainty.
- **Where is the evidence?** Name the visible region or comparison supporting
  the claim.
- **What follows?** State the narrow conclusion justified by the panel.
- **Why does it matter?** Connect the result to the paper's argument.
- **What might be misread?** Identify a tempting but unsupported inference.

Do not jump from “this is Figure 3B” to a conclusion without tracing the
visible evidence.

## Reproducible Crops

When creating crops:

- Record source dimensions and explicit `(left, top, right, bottom)` bounds.
- Preserve panel letters, axes, units, legends, scale bars, and meaningful
  margins.
- Remove neighboring-panel residue or explicitly say what to ignore.
- Store the crop script beside the guide.
- Re-run the script and visually inspect at least one output.

## Attribution and Render QA

Place attribution next to each embedded source figure. Include:

- paper authors or short citation and the figure number;
- canonical paper link and exact version when version drift matters;
- license or other permission basis;
- whether the local image is the complete figure, a crop, or an adapted image.

Before shipping, verify every core figure—not merely one sample crop:

- the local file exists and the Markdown path renders;
- the artwork matches the cited figure and paper version;
- text is readable at the note's normal rendered width;
- panel letters, axes, units, legends, scale bars, and claim-bearing annotations
  are present;
- no neighboring text or panel residue creates a false interpretation;
- an external PDF jump is not required when lawful local embedding is
  available.

## Evidence Boundaries

Label these separately:

- direct observation or reported measurement;
- statistical comparison;
- author interpretation;
- your teaching analogy;
- unresolved ambiguity or limitation.

A teaching diagram may clarify a mechanism, but it is not new experimental
evidence.
