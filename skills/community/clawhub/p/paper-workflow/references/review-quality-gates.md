# Gates

## Purpose

These checks are writing gates. Run them throughout the process, not only at the end.

## Gate 1: Contribution Boundary

- Decide whether the paper is algorithm, system, engineering, demo, empirical, or case-based.
- Ensure title, abstract, intro, method, and conclusion all match that choice.
- Do not mix algorithm-level novelty claims into a systems integration paper unless there is real evidence.

## Gate 2: Evidence Levels

- Label evidence as one of:
  - measured result
  - pilot evidence
  - case evidence
  - future work
- Every claim must match one of these levels.
- Never let planned work appear in results.

## Gate 3: Placeholder Blocking

- No `TBD`, `TODO`, or empty result tables in the main manuscript.
- No placeholder author names, affiliations, or emails.
- No template banner residue or draft markers in submission PDFs.

## Gate 4: Figure-Text Alignment

- Every figure must serve a specific section claim or research question.
- Figure labels, caption text, and body text must use the same terms.
- If the figure changes, update the caption and the body at the same time.

## Gate 5: Naming and Terminology

- Freeze the main system and module names early.
- Use neutral names when brand names create reviewer distraction.
- Keep terminology consistent across text, figures, tables, and appendices.

## Gate 6: Submission Metadata

- Verify authors, affiliations, emails, and corresponding author.
- Verify ethics, data availability, code availability, and funding statements.
- Keep the manuscript metadata aligned with the submission system fields.

## Gate 7: Reviewer Simulation

Use `paper-validator` when a draft is stable enough to inspect. Ask it to check:

- unsupported claims
- missing evidence
- weak novelty articulation
- confusing structure
- stale or thin citations
- figure-text mismatch
- overstated conclusions
