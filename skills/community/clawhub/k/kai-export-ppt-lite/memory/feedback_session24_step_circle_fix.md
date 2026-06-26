---
name: Session 24: Step number circle CSS dimensions + code_bg fix
description: Step circles need CSS width/height (34px) instead of text-based estimation; code_bg shape positioning searches both directions
type: feedback
---

**Step circle fix**: In `build_grid_children` at line 1771 (is_leaf_text_container path), when child has explicit CSS width/height AND visible bg/gradient, use CSS dimensions for both shape and text element bounds. Set `_use_css_dims=True` on text element to prevent layout pass from overriding width in the "short/plain text" branch (line 2287+).

**Why**: Step divs (.step) have CSS `width:34px; height:34px` but text-based estimation gives 0.172"x0.150" vs golden 0.315"x0.315". The layout pass recalculates width for non-block text — need `_use_css_dims` flag to skip recalculation.

**Code bg positioning**: In `position_code_bg_shapes`, search backward FIRST (idx-1 to 0), then forward as fallback. Code_bg shapes are emitted after their sibling text element.

**Result**: Slide 10 6.5→7.3, Slide 3 6.6→6.7. No regressions on other slides.
