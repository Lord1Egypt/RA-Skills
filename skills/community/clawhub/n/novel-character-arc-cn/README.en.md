# Character Growth Arc Card

![Character Growth Arc Card promo](assets/promo-1600x900.png)

Turn scattered character notes into a practical Markdown arc card: desire, flaw, turning point, final choice, and chapter anchors. It is designed for Chinese-language fiction, small-business storytelling, and creator narratives.

## What you get

- Verified facts with source/chapter anchors
- Core desire and flaw
- Four arc stages: start, pressure, turning point, and ending
- A sceneable final choice with its cost
- Chapter-anchor checklist and open questions

The Skill designs a character arc only. It does not continue prose or invent missing facts.

## Input and use

Supply all three inputs: `角色设定` (character profile), `故事概要` (story summary), and `已写章节` (written chapters). A full input is at [fixtures/success/lin-wan.json](fixtures/success/lin-wan.json); a deliberately incomplete input is at [fixtures/failure/missing-chapters.json](fixtures/failure/missing-chapters.json).

Ask a Markdown-Skill-capable writing assistant to follow [SKILL.md](SKILL.md). Existing local field values remain unchanged; inferences are labelled as creative suggestions, and unknowns as items to confirm.

## Self-test

```bash
python3 scripts/self_test.py
```

This validates packaging, metadata, image dimensions, and fixture contracts only. The actual behavior is the Markdown workflow in `SKILL.md`; there is no simulated business engine.

## Source and license

The scoped reference record is in [sources/chinese-novelist-skill.md](sources/chinese-novelist-skill.md). Licensed under [MIT-0](LICENSE).

## Install

```bash
npx skills add xxjrq/novel-character-arc-cn
```

## Complete response examples

See the [success response](fixtures/forward-success.md) and [missing-information response](fixtures/forward-failure.md) alongside the input fixtures.
