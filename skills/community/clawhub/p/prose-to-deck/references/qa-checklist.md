# QA Checklist — Global Pre-Save Verification

Run this checklist after all slides are built, before saving the final HTML.
**Per-slide checks** (one job, headline tier, responsive columns, unused CSS) are handled in the 4.4 per-slide loop — do not repeat them here.
Fix issues silently. Only surface to the user if a fix requires a design decision.

---

## Content (global)

- [ ] Cover contains: title + core thesis + @author (if provided) + scroll indicator
- [ ] Conclusion contains a key takeaway — not a summary of summaries, not new content introduced for the first time
- [ ] The slide sequence has momentum — every slide earns the next; no slide feels like filler
- [ ] `Main claim` is not pasted unchanged as the display headline by default; if it is, that choice is deliberate and justified

## Visual Hierarchy (global)

- [ ] No purple gradient on white — that is the generic AI aesthetic, forbidden
- [ ] Text contrast: primary text ≥ 4.5:1, muted text ≥ 3:1 against background
- [ ] The visual direction from `03-visual-direction.md` is consistent across all slides — same CSS variables, same accent logic, same animation behavior

## Responsive (global)

- [ ] Font sizes use `clamp()` — no fixed `px` on headlines
- [ ] Slide containers use `vw`/`vh` — no fixed pixel widths
- [ ] `@media (max-width: 768px)` block is present
- [ ] For every multi-column layout in the presentation: name the CSS class or selector, and confirm it appears in the `@media (max-width: 768px)` block. If a multi-column layout used inline styles instead of a named class, it must be flagged and a responsive rule added now.

## Technical (global)

- [ ] All external CDN links are present and load in correct order
- [ ] Google Fonts loaded for the roles actually used (Display, Body, and Mono if used)
- [ ] All colors reference CSS custom properties — no hardcoded hex values outside `:root`
- [ ] Every CSS class defined in `<style>` is referenced at least once in the HTML body (no dead CSS)
- [ ] Nav dots count matches the total number of `<section class="slide">` elements
- [ ] Reveal animations trigger on scroll (IntersectionObserver attached)
- [ ] First slide's reveal animations fire on load (setTimeout fallback present)
- [ ] No JavaScript errors from missing DOM elements (IDs match between HTML and JS)

## Shareable Test

- [ ] Identified the single most shareable slide and recorded it in `progress.md`
- [ ] That slide communicates something valuable without surrounding context
- [ ] The shareable slide is strong because of clear visual judgment — not just because a headline was enlarged
