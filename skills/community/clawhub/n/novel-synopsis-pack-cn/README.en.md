# Novel Submission Synopsis Pack

![Novel Submission Synopsis Pack promo](assets/promo-1600x900.png)

Turn existing novel material into editor-ready submission documents: 300-, 800-, and 1,500-character Chinese synopses plus a character-relationship summary, with the ending and causal chain retained.

## What you get

- Three synopsis lengths for common submission requirements
- A concise relationship summary covering conflict and change
- Clear separation of supplied facts, suggestions, and unanswered questions

This is a Markdown-only Skill. It needs no service, third-party API, or login. It organizes supplied material only; it does not score novels, judge market potential, or write chapters.

## Use

Provide a complete story overview, chapter summaries, and submission length requirements. See [fixtures/success.json](fixtures/success.json) for the minimum input. The exact workflow and response shape are in [SKILL.md](SKILL.md).

When required material is absent, it identifies the missing fields instead of inventing story facts; see [fixtures/failure-missing-fields.json](fixtures/failure-missing-fields.json).

## Local check

```bash
python3 scripts/self_test.py
```

The check validates package structure, metadata, asset dimensions, and success/failure fixture shapes only. It does not simulate an LLM or claim to verify synopsis quality.

## Source and license

See [sources.md](sources.md) for the limited-use source note. Licensed under the [MIT-0](LICENSE).

## Install

```bash
npx skills add xxjrq/novel-synopsis-pack-cn
```

## Complete response examples

See the [success response](fixtures/forward-success.md) and [missing-information response](fixtures/forward-failure.md) alongside the input fixtures.
