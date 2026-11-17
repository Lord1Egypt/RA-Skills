# Character Address & Alias Checker (Chinese Fiction)

![Promo](assets/promo-1600x900.png)

Turn pre-publication name and address consistency checks into an anchored, reviewable list. The skill checks character names, aliases, and forms of address only; it does not rewrite dialogue or infer plot and relationship subtext.

## Input and output

Provide a real-name/alias roster for up to 30 characters, approved `speaker → address → target` rules, and text with chapter anchors (up to 100 address mentions). It returns a variant-to-owner table, incorrect or ambiguous mentions, and safe per-location suggestions. Missing alias ownership or speaker identity is marked **Needs confirmation**. Same-name characters remain distinct; no global replacement is proposed.

## Install

```bash
npx skills add xxjrq/novel-name-address-check-cn
```

See the reproducible [success fixture](fixtures/success.md) and [missing-data fixture](fixtures/failure.md). Run `python3 scripts/self_test.py` to verify the included reference checker.

## Source and license

The use case was reviewed against [story-skills character-management](https://github.com/danjdewhurst/story-skills/blob/main/skills/character-management/SKILL.md). This repository's wording, examples, and implementation are original; no external text or source was copied. See [LICENSE](LICENSE).
