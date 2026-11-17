# Novel Research Notes Card

![Novel Research Notes Card promo](assets/promo-1600x900.png)

Turn the excerpts, official links, and setting question you already have into a traceable fiction research card: usable facts, their locations in the source, writing options, and missing evidence. It works only from supplied material; it does not replace evidence with guesses or present historical, medical, or legal conclusions as professional advice.

## Input and output

Provide materials for one chapter, scene, or short piece (pasted text, excerpts, up to 100 table rows, or accessible official URLs) plus a specific setting question. You may include time, place, and narrative intent. The output is a Markdown card with source-located usable facts, clearly labelled creative inferences, evidence limits, and a list of missing materials. Larger inputs are split into batches rather than treated as fully read.

## Install

```bash
npx skills add xxjrq/novel-research-notes-cn
```

## Examples

- [Successful input](fixtures/success-input.md) → [delivery](fixtures/success-example.md)
- [Insufficient-material input](fixtures/failure-input.md) → [delivery](fixtures/failure-example.md)

## Run the self-test

```bash
python3 scripts/self_test.py
```

The test validates local structure and assets only; it does not claim to validate model behavior.

## Source and license

The instructions and examples are original. The use case was informed by [story-skills research](https://github.com/danjdewhurst/story-skills/tree/main/skills/research); its [MIT license](https://github.com/danjdewhurst/story-skills/blob/main/LICENSE) was checked, and no text or code was copied. Licensed under [MIT-0](LICENSE).
