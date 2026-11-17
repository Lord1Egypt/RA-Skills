---
name: excel-to-word-grounded-fill
description: Grounded generation and precision filling of Word documents from Excel data while preserving a supplied Word template's structure and formatting. Use when the user supplies an authoritative .xlsx/.xls/.csv data file, a completed .docx reference example, and a blank or partially populated .docx target, and asks to intelligently draft and insert concise text without inventing facts or mixing the reference example's content into the result.
---

# Excel To Word Grounded Fill

## Purpose

Fill the target Word document from the supplied Excel data. Treat Excel as the only factual source, the completed Word example as a presentation reference, and the target Word file as the output base.

Read [references/grounding-and-qa.md](references/grounding-and-qa.md) before drafting. Apply the available spreadsheet and document artifact workflows for extraction, editing, rendering, and verification.

## Classify the inputs

Identify these roles explicitly before editing:

1. **Data source**: the authoritative Excel workbook or delimited table.
2. **Reference document**: a completed Word example used only for structure, formatting, tone, and level of detail.
3. **Target document**: the blank or partially populated Word file to fill and deliver.

If filenames are ambiguous, inspect all candidates and infer roles from their contents. Ask the user only when two files could plausibly be the target and choosing incorrectly would overwrite or misplace content. Never edit the reference or the source workbook.

## Establish a source map

Inspect every relevant worksheet, merged range, header row, note, unit, footnote, hidden row/column, formula result, and populated target field. Do not rely on a preview alone.

Before drafting, build a temporary source map with:

- target section, paragraph, table cell, or placeholder;
- required meaning;
- exact workbook sheet and cell/range;
- transformation, if any;
- status: supported, missing, ambiguous, or not applicable.

Use workbook values as displayed when formatting carries meaning, including percent signs, decimal precision, date format, signs, units, bases, and labels. Do not silently replace a formula result with a differently recalculated value.

## Separate facts from presentation

Apply this precedence strictly:

1. Excel supplies all case-specific facts and findings.
2. Existing content in the target supplies fixed labels, instructions, and preapproved text unless it is clearly a placeholder.
3. The reference supplies layout, styles, section order, rhetorical pattern, and approximate detail only.

Never transfer names, brands, products, markets, dates, figures, rankings, causal claims, recommendations, or conclusions from the reference. Reuse generic headings only when they fit the current data. Remove or leave unfilled any reference section that the current data cannot support.

## Draft grounded text

Draft only after the source map is complete.

- State the subject and finding directly; use concise professional language.
- Preserve material qualifiers, comparisons, segment differences, sample bases, units, time periods, and exceptions present in the data.
- Combine repetitive rows when no meaning is lost; do not compress away distinct findings.
- Make calculations only when they are deterministic from cited cells and useful for the requested field. Record the formula in the source map and preserve precision appropriate to the workbook.
- Treat blank, `N/A`, `-`, suppressed, and zero as distinct states.
- For missing support, keep the field blank or write `待确认` only when a visible marker is appropriate. Do not guess.
- Do not add causes, implications, recommendations, sentiment, or trend language unless supported by the workbook.

If the reference's narrative conflicts with the current data, follow the current data and rewrite the narrative. Do not imitate sentences by substituting a few nouns or numbers.

## Fill the target document

Edit a copy of the target and preserve its native Word structure. Match the corresponding reference formatting one-to-one where the target expects it, including:

- paragraph and character styles;
- font family, size, color, weight, spacing, indentation, and alignment;
- numbering, bullets, tables, cell shading, borders, and merged cells;
- headers, footers, section breaks, page size, margins, page numbering, and keep-with-next behavior;
- placeholders, content controls, and existing fixed content.

Prefer applying existing styles or cloning corresponding formatting over reconstructing it manually. Replace placeholders without destroying surrounding run formatting. Do not redesign the document unless the user asks.

When the reference contains a section absent from the target, add it only if the target's structure clearly calls for it and the Excel data supports it. The target remains the output base; the reference is not a source document to copy and sanitize.

## Verify before delivery

Perform both semantic and visual verification. Do not deliver after text insertion alone.

1. Trace every case-specific statement, number, comparison, and qualifier in the output to the source map.
2. Compare the output against the reference and search for leaked example-specific names, numbers, dates, findings, or conclusions.
3. Compare the output against the target-before-editing to confirm fixed content was preserved.
4. Recheck all relevant workbook fields for omissions and confirm missing values were not converted into claims.
5. Render the output Word file to page images or PDF and inspect every page for overflow, clipping, bad wrapping, broken tables, altered pagination, orphan headings, and style drift.
6. Iterate until content and layout checks pass.

Deliver the filled `.docx`. In the handoff, identify any fields left blank or marked `待确认` and briefly state why. Do not claim complete validation if any page could not be rendered or inspected.
