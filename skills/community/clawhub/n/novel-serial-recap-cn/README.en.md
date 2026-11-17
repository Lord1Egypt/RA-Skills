# Chinese Serial Story Recap

![Chinese Serial Story Recap](assets/promo-1600x900.png)

Turn recent chapter text or summaries and a next-chapter goal into two useful documents: a 120–250-character Chinese recap for readers and a continuation memory card for the author. Keep character states, causes and unresolved clues without inventing new story events.

## Input and output

Provide recent chapter material in order and the goal for the next chapter. The memory card separates known facts, current character states, unresolved clues, suggested transition points and unanswered questions.

This is a Markdown Skill with no browser, account or additional service requirement. It organizes supplied chapters and does not write a new chapter or plan an entire book.

## Use

Invoke `$novel-serial-recap-cn` with your material. See [SKILL.md](SKILL.md) for the workflow, [success input](fixtures/success-input.md) for a complete example and [missing-goal input](fixtures/failure-missing-goal.md) for the incomplete case. Missing chapter material or goals should be requested before generation.

## Install

```bash
npx skills add xxjrq/novel-serial-recap-cn
```

## Local check

```bash
bash scripts/self-test.sh
```

The offline check verifies package structure, metadata, asset dimensions and input examples. Generated prose is reviewed separately against the supplied chapter facts.

## Sources and license

The original workflow is licensed under [MIT-0](LICENSE). Public use-case references are recorded in [sources.md](sources.md).

## Complete response examples

See the [success response](fixtures/forward-success.md) and [missing-information response](fixtures/forward-failure.md) alongside the input fixtures.
