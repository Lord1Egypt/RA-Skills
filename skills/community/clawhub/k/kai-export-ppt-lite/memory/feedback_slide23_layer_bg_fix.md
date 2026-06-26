---
name: Session 23: Root cause of missing card bg shapes on Slides 3/6/7
description: .layer elements going through flatExtract→build_grid_children (not via grid/flex-column path) don't get bg shapes created
type: project
---

**Root cause**: Slide 3 (and Slides 6, 7) `.layer` elements have `display:flex` (flex-row default) with no `flex-direction:column`. They go through `flatExtract` line 1293 → `build_grid_children` because `_detect_flex_row` returns True.

Inside `build_grid_children`, `.layer` is treated as a flex-row with `num_cols = len(children) = 2` (div.step + div). Children go through the standard loop (lines 1547-1749). **No bg shape is created for the `.layer` container itself.**

The bg shape creation code at lines 1710-1722 is ONLY triggered when a flex-row is INSIDE a flex-column container that's inside a grid container (the `is_cc_flex_row` path at lines 1647-1731).

Standalone flex-row containers (like Slide 3's `.layer`) never create their own bg shape.

**Fix**: In `flatExtract` at line 1293-1306, when `_detect_flex_row` returns True and the container has visible bg/border, create a bg shape and prepend it to the grid_children results.

**Golden comparison**: Slide 3 missing 8 shapes including 2 card_bg (w=7.591", h=0.813"/1.258"), 2 border-left accents (w=0.185", h=0.813"), 2 decoration shapes, 2 pill bg shapes.
