# Line Length Optimizer

**Check or fix the reading measure (line length) of a text block.**

Verifies a paragraph or container sits in the typographically comfortable range — 45–75 characters per line on desktop, 35–45 on mobile — and produces a concrete `ch`-based CSS fix when it doesn't.

## What it does

- Measures or estimates characters-per-line from a text block, a container width + font-size, or a live Figma text node.
- Compares against the standard measure range (Bringhurst: 45–75 desktop, 65 as the sweet spot; 35–45 mobile).
- Recommends `max-width: NNch;` (preferred over fixed `px`, since `ch` scales with font) or flags when the container has no fixed width to check (Figma auto-width text).
- With Figma access: reads `textNode.textAutoResize`, `fontSize`, and font family to compute the fix, and can resize the node directly on explicit request.

## When to use

- Reviewing a container/component holding body copy for readable width.
- User pastes a paragraph or gives a width/font-size and asks if it's in range.

## When NOT to use

- Headings, buttons, labels — measure only matters for wrapping prose.
- Full type-scale or vertical-rhythm work — see the related skills below.

## What's inside

```
line-length-optimizer/
├── README.md    ← this file
├── SKILL.md     ← full workflow, Figma integration, quality checklist
└── LICENSE      ← MIT
```

## Related skills

Part of a small typography/layout family in this playbook: this skill sets column width, [`text-typesetting`](../text-typesetting/README.md) sets line-height/tracking, [`vertical-spacing`](../vertical-spacing/README.md) sets rhythm between blocks, and [`microtypography`](../microtypography/README.md) applies character-level fixes last (ragged-edge risk depends on the measure this skill sets).

## License

MIT — see `LICENSE`. Author: **[Monika Zapisek](https://monikazapisek.com)**. Project: **Design Engineering Playbook**.

---

*Part of the [Design Engineering Playbook](https://github.com/monikazapisek/design-engineering-playbook) — AI-assisted workflow artefacts for product designers working in agile and lean environments.*
