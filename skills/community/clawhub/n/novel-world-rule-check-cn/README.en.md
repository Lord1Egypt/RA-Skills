# World Rule Conflict Table

Catch continuity problems in abilities, costs, and exceptions by checking chapter text against the author's approved rules. Provide numbered rules and short excerpts; receive an evidence-linked table of pass, conflict, or insufficient information, plus revision choices that require author approval. Missing rules are requested rather than invented from genre conventions.

## Input and result

Supply up to 20 approved rules (`id`, trigger, cost, exceptions) and up to 10 short scenes. The result maps each rule to quoted text, a verdict, evidence, and author-approved revision options, with missing fields called out. This Skill audits approved rules only; it does not create worldbuilding or add exceptions.

## Install

```bash
npx skills add xxjrq/novel-world-rule-check-cn
```

See [SKILL.md](SKILL.md) for the input format and review method. Copyable [successful](fixtures/success.md) and [missing-input](fixtures/failure.md) deliveries are included.

## Self-test

Run `python3 scripts/self_test.py` from this repository. It uses no network, sibling Skill, or machine-specific path.

## Source and license

The public [story-skills worldbuilding Skill](https://github.com/danjdewhurst/story-skills/blob/main/skills/worldbuilding/SKILL.md) informed the business use case only. Instructions and examples here are original. Licensed under [MIT-0](LICENSE).
