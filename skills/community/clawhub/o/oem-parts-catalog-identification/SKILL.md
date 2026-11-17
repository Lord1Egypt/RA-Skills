---
name: "oem-parts-catalog-identification"
description: "Identify OEM part numbers from PDF parts catalogs by matching vehicle scope, exploded positions, and parts-table entries."
---

# OEM Parts Catalog Identification

## Use when
Identify an OEM vehicle part number from a PDF catalog, especially when the requested component may be sold only as an assembly.

## Procedure
1. Establish the exact vehicle scope: model, build years, engine/version, and any chassis prefixes available.
2. Prefer a catalog whose title and internal header match that scope. Treat search snippets as discovery evidence, not the final part-number source.
3. Download the PDF to a temporary file.
4. Run `pdfinfo` to confirm it is a readable PDF and note its page count.
5. Extract text with `pdftotext -layout`. Search the index and body for the subsystem and likely synonyms, such as `front fork`, `fork tube`, `inner tube`, or `stanchion`.
6. Re-extract only the relevant page range with `pdftotext -f … -l … -layout` so headers, positions, codes, descriptions, quantities, and variants remain together.
7. Match the exploded-diagram position to the parts-table row. Record side, quantity, and variant rather than trusting the description alone.
8. Decide whether the requested item has its own row. If not, report the smallest listed assembly that contains it; do not invent a standalone number.
9. If text extraction leaves position or side ambiguous, render the relevant pages with `pdftoppm` and inspect the diagram before answering.
10. Clean temporary files with the available safe-delete mechanism. If `trash` is unavailable, check for `gio`; the evidenced fallback is `gio trash <path>`.

## Pitfalls
- Catalog year ranges can contain different engines or chassis families.
- Search-result snippets can expose codes without proving applicability.
- Translated descriptions may be inconsistent; position, side, quantity, and diagram provide stronger context.
- A tube, housing, or internal component may appear only inside a fork-leg or larger assembly.
- A cleanup failure does not invalidate successful PDF extraction; preserve the result, switch cleanup mechanism, and verify cleanup separately.

## Verification
Before answering, confirm all of these from the catalog itself:
- model/year or chassis header matches the target;
- subsystem/table title matches the requested area;
- diagram position and table position agree;
- code, side, quantity, and variant are internally consistent;
- any claim that a part is not sold separately follows from the absence of its own row and the presence of the containing assembly.

Cite the catalog URL and relevant PDF pages in the result.
