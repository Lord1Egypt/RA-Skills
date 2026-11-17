---
name: "ieee-referencing"
description: "IEEE numeric referencing for engineering and CS: bracketed citation order, numbered references, doi format. Use for papers requiring IEEE style."
---

# IEEE Referencing

Build IEEE-style numeric citations: bracketed numbers in the text ordered by first appearance, a references list numbered in that same order (not alphabetical), and the IEEE punctuation conventions that generic tools get wrong.

## Steps

1. Read `references/ieee-quickref.md`, then number citations in order of first appearance: `[1]`, then `[2]`, and so on. Cite multiple works as `[1], [3]-[5]`. Place the number before punctuation when possible; a sentence ending in a citation reads `... as shown in [2].`

2. Match the source type:

   - Journal: `A. A. Author, "Title of paper," Journal Name, vol. x, no. x, pp. xx-xx, Month Year, doi: 10.xxxx/xxxxx.`
   - Book: `A. A. Author, Title of Book, xth ed. Place: Publisher, Year.`
   - Chapter: `A. A. Author, "Title of chapter," in Book Title, E. Editor (Ed.). Place: Publisher, Year, pp. xx-xx.`
   - Web: `A. A. Author. "Page title." Site Name. URL (accessed Month Day, Year).`

3. Apply the IEEE signatures:
   - Authors: initials before surname (`A. A. Author`), all authors listed or `et al.` for six or more
   - Paper and chapter titles in double quotation marks; journal and book titles in italics
   - Abbreviated units: `vol.`, `no.`, `pp.`, `ed.`
   - `doi: 10.xxxx/xxxxx` lowercase prefix, no https wrapper
   - Access date in parentheses for web sources

4. The references list is ordered by citation number, never alphabetical. Each entry begins its bracket number: `[1] A. A. Author, ...`

5. Verify: numbers run `[1]...[n]` with no gaps, every bracketed number in the text has an entry, first-appearance ordering holds, and no entry is cited that is not referenced.

## Pitfalls

- Alphabetizing the reference list is the classic IEEE failure; order follows first citation.
- Author name order inverts vs APA/MLA: initials first, surname last, no comma between.
- Conference papers use: `A. A. Author, "Title," in Proc. Conf. Name, City, Year, pp. xx-xx.`
- Standard numbers cite as: `IEEE Standard for X, IEEE Std 1234-2024, Year.`

## Provenance

Clean-room summary of IEEE Editorial Style Manual conventions for agent use, authored 2026-09-03. Part of the referencing skill family with `apa-7-referencing`, `harvard-referencing`, `oxford-referencing`, and `mla-referencing`.