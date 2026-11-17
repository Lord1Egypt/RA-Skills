# Microtypography

**Polish and English microtypography pass for body copy — before it publishes.**

Fixes the small stuff that separates typeset text from a raw text dump: hanging single-letter conjunctions (`i`, `w`, `z`, `a`...), widow/orphan risk at paragraph ends, dimension/unit formatting (`1920×1080`, `100 PLN`), smart dashes and language-correct quotation marks, and ragged-edge handling for both hard-wrapped and reflowing text.

## What it does

- **Hanging conjunctions/prepositions** — non-breaking space so a single-letter PL word (or `a`/`I` in EN strict mode) never ends a line.
- **Numbers, units, dimensions** — proper `×` in dimension pairs, NBSP between number and unit/currency, en dash in numeric ranges.
- **Functional Unicode spacing** — narrow no-break space for supported number–unit/grouping cases, figure space for blank digit positions, thin/hair spaces only for inspected optical corrections, and non-breaking hyphen only where a split would be harmful; compatibility falls back to NBSP or the original character.
- **Smart punctuation** — straight quotes → language-correct typographic quotes (`„...”` PL, `“...”` EN); double hyphens → en/em dash.
- **Widow/orphan guard** — last two words of every paragraph bound with NBSP; widow risk near page/column breaks flagged, not guessed at.
- **Ragged edges** — Case A (hard-wrapped text): recomputes the wrap with a minimal-raggedness pass. Case B (reflowing HTML/markdown): inserts soft hyphens on long unbreakable words and reports a CSS fix (`hyphens: auto`, `text-wrap: pretty`), since the source can't control browser line breaks directly.
- **Figma mode** — reads selected text nodes, skips variable- or component-property-driven copy, preserves mixed range styles with `deleteCharacters` / `insertCharacters`, and can set native wrapping or hanging punctuation only after reporting the change.
- Reads first and asks only when a missing value changes the result; every Figma write requires permission.

## When to use

- Before publishing a blog post, landing page, case study, or any long-form markdown/HTML copy.
- User asks to fix hanging conjunctions, "sieroty i wdowy", or run a typography/typesetting pass.

## When NOT to use

- Code, tables, short UI labels, single-line strings — there's no line-wrap to protect.
- Content rewrites — this is a typesetting pass, not a copy edit. Wording is never altered beyond what orphan-joining requires.

## What's inside

```
microtypography/
├── README.md          ← this file
├── SKILL.md            ← full workflow, rules, and quality checklist
├── LICENSE             ← MIT
└── examples/
    └── test-results.md ← dry-run test cases (PL/EN, Case A/B ragged-edge)
```

## Related skills

Part of a small typography/layout family in this playbook:
[`line-length-optimizer`](../line-length-optimizer/README.md) (column width) → [`text-typesetting`](../text-typesetting/README.md) (line-height/tracking) → [`vertical-spacing`](../vertical-spacing/README.md) (rhythm between blocks). Apply `microtypography` last, since column width and font choices upstream affect where its ragged-edge rules actually bite.

## License

MIT — see `LICENSE`. Author: **[Monika Zapisek](https://monikazapisek.com)**. Project: **Design Engineering Playbook**.

---

*Part of the [Design Engineering Playbook](https://github.com/monikazapisek/design-engineering-playbook) — AI-assisted workflow artefacts for product designers working in agile and lean environments.*
