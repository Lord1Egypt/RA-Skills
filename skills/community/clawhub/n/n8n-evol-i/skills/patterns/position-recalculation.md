---
name: pattern-position-recalculation
description: When inserting nodes mid-flow, shift downstream nodes 220px right.
user-invocable: false
---

# Pattern: position recalculation

n8n's canvas uses `position: [x, y]` integer coordinates per node. When you insert a node mid-flow, downstream nodes overlap visually unless you shift them.

## Rule

For every node inserted at horizontal position `x`, shift every downstream node's `x` by 220 pixels (the canonical n8n grid step).

## Helpers that apply this

`add-lock-to-workflow.md`'s `add_lock_to_workflow.py` does this internally: when it inserts `Lock Acquire` (one node) and `Lock Release` (another node), it shifts every existing non-trigger node's `x` by 440 pixels (220 × 2) to make room.

## When you write your own helper

```python
def shift_right(nodes, x_threshold, by=220):
    for n in nodes:
        pos = n.get("position") or [0, 0]
        if pos[0] >= x_threshold:
            n["position"] = [pos[0] + by, pos[1]]
```

This keeps the canvas legible after edits.
