# Figure integrity deep-fix notes

## Session class
Paper-based journal club PPT repair after user flagged two hard defects:
1. figure aspect ratio was distorted
2. crops still cut into real content

## What changed
- Switched from fixed width+height picture placement to aspect-ratio-preserving `contain` placement.
- Added extra inner padding inside picture frames so rendered PPT/PDF output would not clip figures that looked safe in source.
- Re-cropped pages more conservatively, explicitly trimming away page-edge black bars/artifacts while keeping more top/bottom margin around figure bodies.
- Repeated real render QA (`soffice --headless` -> PDF -> `pdftoppm`) after each crop/layout adjustment.
- Dense right-side support images sometimes remained unreadable even after safe crops; lesson is that “safe” and “readable” are separate checks.

## Practical workflow lesson
1. Fix aspect ratio first.
2. Re-render and inspect for clipping in the rendered output, not just in source coordinates.
3. If clipping remains, widen crop and remove page-edge artifacts.
4. If the wider crop becomes unreadably small, do not squeeze it back into the same footprint by unsafe cropping; instead enlarge the support region, reduce nearby text burden, or split the figure onto a cleaner layout.
5. Only call the deck fixed after rendered QA shows no clipping on the previously broken pages.

## Useful indicators during QA
- y-axis titles truncated at the top/left edge
- panel headers glued to the top border
- right-edge black strips obscuring page content
- support pages that are technically complete but visually unreadable after shrink
- text boxes whose last line gets clipped after PPT export
