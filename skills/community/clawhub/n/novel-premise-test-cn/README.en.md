# Novel Premise Viability Test

Decide whether a novel idea can carry a story before drafting. This skill turns one premise into a central conflict, stakes, theme, and three development paths—and names missing inputs instead of inventing them.

![Novel Premise Viability Test promo](assets/promo-1600x900.png)

## Install

```bash
npx skills add xxjrq/novel-premise-test-cn
```

## Use

```text
Use $novel-premise-test-cn to assess the premise below. Separate supplied facts from unconfirmed goals, motives, and consequences. Label all three development paths as suggestions.
```

Provide one premise, a genre, and a target readership. You receive a viability verdict, a one-sentence premise, central conflict, stakes, theme, three distinct paths, and a next step. If any required field is missing, the response lists what to add.

A discovered event does not imply a decision to investigate. If the character's goal is absent, the verdict is “needs tightening” and the goal remains unconfirmed.

This is for a chapter-, scene-, or short-work-scale premise. Tables are limited to 100 rows; send longer material in batches. It does not generate an opening hook or manage a full novel.

Copyable examples: [successful input](fixtures/success-input.md), [successful delivery](fixtures/success-output.md), [missing-input example](fixtures/failure-input.md), and [missing-input delivery](fixtures/failure-output.md).

## Self-test

```bash
python3 scripts/self_test.py
```

The command runs from this repository and checks only local metadata, fixtures, and asset dimensions.

## Source note and license

The workflow and examples are original. The public [story-skills repository](https://github.com/danjdewhurst/story-skills) was consulted only for business context; no external text or code is included. Released under the [MIT-0](LICENSE).
