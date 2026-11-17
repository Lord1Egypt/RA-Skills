## Description:

Polymarket Worldcup Watcher monitors Polymarket World Cup winner markets, scans 100+ national team markets, and alerts when odds move by more than 0.5%.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sg345662365-oss](https://clawhub.ai/user/sg345662365-oss)

### License/Terms of Use:

MIT-0

## Use Case:

Prediction-market traders and monitoring agents use this skill to track World Cup winner odds, compare baseline movements, and receive Telegram alerts for notable price changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram alerts may reveal trading interests or market activity.

Mitigation: Use a private Telegram bot or chat for alerts, as recommended by the server security guidance.

Risk: The skill depends on installing and running a ClawHub package that monitors an external prediction-market API.

Mitigation: Confirm the package source and version in ClawHub before installation, and avoid granting broader filesystem, credential, or account permissions than the monitor needs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sg345662365-oss/skills/polymarket-worldcup-watcher)
- [ClawHub publisher profile](https://clawhub.ai/user/sg345662365-oss)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with alert text examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces odds-monitoring guidance and Telegram alert content for Polymarket World Cup markets.]

## Skill Version(s):

2.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
