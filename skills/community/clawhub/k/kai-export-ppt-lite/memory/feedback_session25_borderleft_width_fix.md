---
name: Session 25: borderLeft info bar width fix through layout sync
description: borderLeft accent shapes (like .info bars) need full slide width, not paired text width. Three-point fix prevents post-layout sync from overriding.
type: feedback
---

**Problem**: `.info` divs with `border-left: 4px solid var(--accent-blue)` should render as full-width bars (~9.16") in the golden reference, but sandbox was producing 7.96" shapes matching the text width only.

**Root cause**: The width fix in `flat_extract`'s `all_inline` path correctly calculated 9.16" (line 1522), but a **post-layout sync pass** at line ~2868 (`layout_slide_elements` end) unconditionally synced ALL paired shape widths to their text element widths: `sb['width'] = tb['width']`. This overrode the pre-computed expanded width.

**Fix in 3 places**:

1. **`flat_extract` all_inline path** (line ~1522): For shapes with `4px` border-left accent, set `shape_w = max_w_in * 1.15` (full content width). Changed check from `not bl.startswith('0px')` to `'4px' in bl` to avoid matching thin borders like `1px solid rgba(...)`.

2. **`layout_slide_elements` paired shape handler** (line ~2779): Same `'4px' in bl` check to apply expanded width during layout pass.

3. **Post-layout sync pass** (line ~2871): Skip width sync for border-left accent shapes:
   ```python
   bl = elem.get('styles', {}).get('borderLeft', '')
   if bl and 'none' not in bl and '4px' in bl:
       continue  # keep pre-computed width
   sb['width'] = tb['width']
   ```

**Key insight**: The border-left check must specifically match `4px` (the CSS accent bar thickness), not just any non-zero border. Thin borders from `border` property like `1px solid rgba(37,99,235,0.20)` were being incorrectly matched by the broader `not bl.startswith('0px')` check, causing regressions on Slide 1 stat cards.

**Result**: Slide 2 info bar width 7.96" → 9.16". No regressions on other slides.
