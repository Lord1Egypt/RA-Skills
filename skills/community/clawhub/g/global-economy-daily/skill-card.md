## Description:

Automatically generate and send daily global economic insight reports with market data, geopolitical news, and outlooks via QQ or Feishu.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markdown777](https://clawhub.ai/user/markdown777)

### License/Terms of Use:

MIT-0

## Use Case:

Agents or operators use this skill to produce a daily global economy briefing covering markets, commodities, foreign exchange, crypto, and geopolitical events, then manually run or schedule delivery to QQ or Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill documents persistent scheduled execution through a macOS LaunchAgent.

Mitigation: Only enable scheduled execution intentionally and keep an unload or removal process available.

Risk: A bundled QQ recipient could misdirect reports if delivery is enabled without review.

Mitigation: Remove or replace the bundled QQ recipient and confirm the resolved destination with a dry run before enabling QQ or Feishu delivery.

Risk: Generated market and geopolitical outlooks may be incomplete, stale, or unsuitable for decision-making on their own.

Mitigation: Review the report and source data before acting on its conclusions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/markdown777/skills/global-economy-daily)
- [Yahoo Finance Chart API](https://query1.finance.yahoo.com/v8/finance/chart)
- [Artifact Skill Documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown report text with optional shell commands and configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Yahoo Finance market data and configurable QQ or Feishu delivery settings.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
