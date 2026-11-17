## Description:

Polymarket market probability movement detection that scans prediction-market probability fluctuations, explains likely movement causes, and helps users manage movement alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cnica](https://clawhub.ai/user/cnica)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to find Polymarket markets with large recent probability changes, review possible news drivers, and create or manage saved movement-alert settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill queries Polymarket-related data and uses web search to explain market moves.

Mitigation: Confirm users are comfortable with those data lookups before installation, and cite source links or mark explanations as unverified speculation when no relevant source is found.

Risk: Alert settings are stored locally in the skill directory.

Mitigation: Treat saved alerts as user preferences and run checks only when the host agent explicitly performs alert-check behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cnica/skills/polymarket-predictradar-market-movers-skills)
- [Publisher profile](https://clawhub.ai/user/cnica)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown movement leaderboards, alert confirmations, and alert summaries with links when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local alert configuration records and cited source links for market-movement explanations.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
