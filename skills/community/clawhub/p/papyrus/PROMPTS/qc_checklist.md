# Quality Control Checklist — Three-Round Review

> Run these checks before delivering any Papyrus output.

## Round 1: Structure 🔍

- [ ] All paper sections present (Abstract → Introduction → ... → References → Appendix)
- [ ] Table of Contents page generated and correct
- [ ] Every original figure has a corresponding image in the PDF
- [ ] Figure source files match the arXiv HTML figure mapping (NOT guessed)
- [ ] All displayed formulas have a formula-block container
- [ ] No blank/empty pages
- [ ] Page numbering appears on all pages
- [ ] Cover page renders without content overlap

## Round 2: Content 📝

- [ ] English text in `.english-text` blocks matches the original paper verbatim
- [ ] Chinese translation in `.chinese-text` blocks is accurate and natural
- [ ] Each commentary block adds insight (not just restating)
- [ ] No fabricated information in commentary blocks
- [ ] Figure captions match the paper's actual Figure N labels
- [ ] Table data (numbers, percentages, BLEU scores) matches paper exactly
- [ ] All `<strong>` tags are on semantically meaningful terms (NOT structural labels like "Encoder:", "Decoder:")
- [ ] Footnote content preserved where relevant

## Round 3: Visual Quality 🎨

### Formulas
- [ ] All formula images are sharp (no pixelation or blur)
- [ ] Formula images use native resolution — no CSS height-based scaling
- [ ] Long formulas (e.g., MultiHead, lrate) fit within the wireframe box without overflow
- [ ] Short formulas are centered with proper left/right whitespace
- [ ] The wireframe box (border + background) is visible and consistent across all formulas
- [ ] Fraction lines, summation symbols, square roots are complete and correct
- [ ] Superscripts and subscripts are clearly readable

### Images & Figures
- [ ] All embedded images display at appropriate sizes
- [ ] Figure quality is not degraded by compression or scaling
- [ ] Multi-panel figures are displayed correctly (side-by-side when in original)
- [ ] Figure backgrounds blend with page background

### Typography
- [ ] Chinese text renders in MingLiU (or fallback: LiSong Pro → SimSun)
- [ ] English text renders in Times New Roman
- [ ] Math symbols render in Cambria Math
- [ ] No font substitution artifacts (□ boxes, tofu characters)
- [ ] Line spacing is consistent throughout
- [ ] Headings are visually distinct from body text
- [ ] Commentary blocks have visible left border and background

### Page Layout
- [ ] Margins are consistent on all pages
- [ ] No orphan/widow lines (single lines at page top/bottom)
- [ ] Tables don't break across pages mid-row
- [ ] Formula blocks don't break across pages
- [ ] Bilingual blocks stay together on the same page

## Common Errors (from past sessions)

| Error | Cause | Fix |
|-------|-------|-----|
| Blurry formulas | PNG images upscaled with LANCZOS | Use native resolution, `height:auto` |
| Formula overflow | Fixed CSS height ignoring aspect ratio | Use `max-width:100%; height:auto` |
| Wrong figures | Guessing ModalNet filenames | Check arXiv HTML source `<figure>` blocks |
| Missing appendix figures | x*.png not downloaded | Fetch from `arxiv.org/html/.../xN.png` |
| Broken math SVGs | WeasyPrint can't render complex SVG | Always use codecogs PNG for formulas |
| Double `<strong>` tags | Structural labels bolded | Only bold semantic key terms |
| Font issues on macOS | MingLiU not available | Fallback chain in CSS font-family |
