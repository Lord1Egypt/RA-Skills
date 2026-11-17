## Description:

Generates Chinese-language daily A-share investment research notes by collecting market data, using available IMA knowledge-base history, and structuring market signals, watchlist tracking, and action plans.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jlfan966-tech](https://clawhub.ai/user/jlfan966-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to generate daily Chinese A-share research notes that combine market data, investment-philosophy prompts, and optional IMA knowledge-base history. It is intended for personal research-note drafting and review, not as a substitute for independent investment judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated notes may contain portfolio views, watchlists, or trading plans and may be saved to a fixed local path or synced to a named IMA knowledge base.

Mitigation: Review the configured output path, IMA destination, and note contents before use, especially when notes include private financial information.

Risk: Market-data connectors or IMA retrieval may be unavailable, incomplete, or in conflict, which can affect the resulting research note.

Mitigation: Check source labels and verify important market data independently before relying on the note for investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jlfan966-tech/skills/guigui-touyan)
- [Server-resolved GitHub provenance](https://github.com/jlfan966-tech/guigui-touyan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown research note with structured sections and optional local file or IMA knowledge-base sync]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses A-share market data connectors and an optional IMA knowledge-base connector; generated notes use a date-stamped filename when written locally.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
