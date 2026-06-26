# Block Model

This skill translates source documents as anchored blocks. The translator must detect source blocks first, assign anchors, then emit exactly one translated block for each source block.

## Anchor Scheme

- Anchors use `P{page}-B{block}` form, for example `P2-B4`.
- `page` is the source page number as seen by the reader.
- `block` is the reading-order block index within that page.
- The same anchor must appear on the translated counterpart of that source block.

## Allowed Block Types

- `title`: Standalone heading or report title.
- `paragraph`: Continuous prose paragraph or short prose section.
- `list`: Ordered or unordered list region.
- `key_value`: Labeled fields such as `Name:`, `DOB:`, `Diagnosis:`.
- `table`: Grid-like tabular content with rows and columns.
- `signature`: Signature line, stamp line, signer/date attestation, or approval line.
- `header_footer`: Repeated running header or footer content that exists in the source.
- `image_adjacent_text`: Text that is inseparable from a nearby image, figure, stamp, or diagram for local reading.

## Hard Mapping Rules

- One source block maps to one translated block. No exceptions.
- Block type must be preserved. A source `table` must remain a `table`; a source `paragraph` must remain a `paragraph`.
- No cross-block relocation. Content from `P2-B4` cannot be moved into `P2-B5` or any other block.
- No block merging. Two adjacent source paragraphs remain two translated paragraph blocks.
- No block splitting for readability. One source paragraph remains one translated paragraph block.
- Reading order must stay aligned with the source document.
- Repeated source headers and footers may be preserved as `header_footer` blocks when they appear in the source; they must not absorb body content.
- `image_adjacent_text` is only for text that depends on local visual adjacency. It must not be used to hide ordinary paragraphs or tables.

## Block Classification Notes

- Use `title` only for headings that function as titles or section headers in the source.
- Use `list` only when the source is visually or structurally a list. Sentence fragments inside prose stay `paragraph`.
- Use `key_value` for field/value layouts even when the source is not a perfect grid.
- Use `table` for row/column structures, including lab panels and medication grids.
- Use `signature` for clinician names, signatures, seals, dates, and sign-off statements grouped as an attestation block.
- Use `header_footer` only for running material such as page headers, page numbers, and institution footer lines.

## Minimal Example

- `P1-B1` -> `title`
- `P1-B2` -> `key_value`
- `P1-B3` -> `paragraph`
- `P1-B4` -> `table`
- `P1-B5` -> `signature`
