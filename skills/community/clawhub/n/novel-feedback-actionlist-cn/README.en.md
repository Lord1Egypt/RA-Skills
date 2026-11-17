# Reader Feedback Revision Action List

Turn supplied reader or editor feedback plus chapter summaries into an actionable revision list. The skill groups duplicate issues, identifies supported chapter impact, prioritizes edits, and preserves evidence. It never invents feedback or re-scores a work.

## Input and output

Provide feedback already received and a chapter number/title/summary for one chapter, scene, or short text. You receive deduplicated issue groups, affected chapters, prioritized revision actions with completion criteria, and clearly stated missing information. Submit material over 100 table rows in batches.

## Install

```bash
npx skills add xxjrq/novel-feedback-actionlist-cn
```

See the copyable [success example](fixtures/success.md) and [missing-material example](fixtures/failure.md). Run `python3 scripts/self_test.py` to validate the standalone package.

## License and source note

This is an original Chinese workflow. It only consulted the purpose of [story-skills feedback-triage](https://github.com/danjdewhurst/story-skills/blob/main/skills/feedback-triage/SKILL.md); no text or code was copied. Licensed under [MIT-0](LICENSE).
