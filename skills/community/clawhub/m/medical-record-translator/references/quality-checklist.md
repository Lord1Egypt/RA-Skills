# Quality Checklist

Use this checklist before delivering the primary artifact.

## Structural Fidelity

- Every source block has exactly one translated block and every translated block has exactly one source anchor.
- Anchors follow `P{page}-B{block}` and remain stable from detection through final output.
- Output block order matches source reading order.
- No source blocks were merged, split, dropped, or duplicated.
- Block types were preserved exactly: `table` stayed `table`, `key_value` stayed `key_value`, `paragraph` stayed `paragraph`, and so on.

## Rendering Integrity

- Paragraph blocks preserve paragraph boundaries and are not rewritten into summaries.
- List blocks preserve item count and item order.
- Key-value regions are rendered as stable structured tables, not as prose or bullets.
- Table regions were not converted into prose, sentence lists, or simplified summaries.
- Embedded HTML was used only when Markdown could not preserve the required table structure.
- Chinese text appears first and the original appears immediately below or beside it within the same anchored block.

## Clinical Readability

- The artifact reads like a faithful bilingual medical record, not a narrative report.
- Terminology is clinically appropriate and consistent with the source context.
- Signatures, dates, dosages, units, abnormal markers, and similar high-risk details remain tied to their original blocks.
- Header/footer content is preserved only when present in the source and not confused with body content.

## Low-Confidence Handling

- Uncertainty is marked inline at the smallest useful scope: phrase, field, or cell.
- Local uncertainty is not inflated into document-wide warnings unless clinically necessary.
- The trailing `需重点核对项` section appears only when clinically important low-confidence items remain.
- Each item in `需重点核对项` references its source anchor and states why review matters clinically.

## Case Review Prompts

- Can the main diagnosis be found without reading the original first?
- Are lab tables still readable as tables?
- Are dates, signatures, and institution names still located in their own blocks?
- Are all low-confidence items traceable to page/block anchors?

## Final Prohibitions Check

- No information-summary, terminology-reference, or other invented primary-artifact sections were added.
- No old report-style framing or required metadata table was reintroduced.
- No cross-block relocation occurred.
- The final artifact is structure-preserving and doctor-readable.
