# Heirloom Provenance — Family Object Storyteller

**The stories die with their keepers. Capture them first.**

Every family has a drawer of objects nobody can explain anymore: the pocket
watch, the odd ceramic, the medal in a language nobody reads. When the
keeper dies, the story dies too — and estates get settled by people who
don't know the worthless-looking chair survived the fire, or that two
siblings have silently wanted the same ring for twenty years.

This is a provenance system for family objects, 100% local:

- **Registry** — origin, owner chain, append-only dated stories, value,
  condition, photo refs. Uncertainty is first-class ("maybe carried in a
  war — which war unknown" is a *better* record than a confident guess)
- **Interview kit** — 7 core questions that unlock stories instead of
  facts, whole-collection walk-through scripts, audio-first workflow with
  transcript linking. Use it NOW, at holidays, during downsizing — not
  after the funeral
- **Estate-ready reports** — provenance sheet per object formatted for
  executors, appraisers, and insurance schedules
- **Storybook export** — the whole registry as readable narrative; the
  second keeper is how a story gets saved
- **Printable tags** — DO-NOT-DISCARD labels with QR payload linking the
  physical object to its record; a registry unlinked from the object dies
  at the first house move
- **Distribution fairness** — sealed wish-lists (collected before any
  reveal, so nobody anchors), conflict detection (dual-#1 surfaced *before*
  the family meeting), seeded rotation draft maximizing top-wish
  satisfaction, equalization payments for value gaps only — stories are
  not priced

## Quick start

```bash
python3 scripts/heirloom.py object add "Grandfather's pocket watch" \
    --origin "c.1920s Zurich" --owners "Otto > Maria" --value 450 \
    --story "Otto traded a rifle for it after WWI."
python3 scripts/heirloom.py interview "Aunt Maria"     # the 7 questions
python3 scripts/heirloom.py wish add HL001 --by Sam --rank 1
python3 scripts/heirloom.py conflicts
python3 scripts/heirloom.py draft --people Sam,Alex --seed 7
python3 scripts/heirloom.py storybook > family_storybook.md
```

Families consistently report the same regret after a death: "we never
asked." This tool exists to make that question a command.

MIT © 2026 Denis Voronin
