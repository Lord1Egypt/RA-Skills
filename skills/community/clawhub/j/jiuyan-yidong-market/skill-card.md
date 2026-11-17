## Description:

Automatically browses Jiuyan Gongshe market movement data and produces structured Chinese market briefs covering market environment, opportunities, risks, hot sectors, and leading stocks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajian11](https://clawhub.ai/user/ajian11)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and market-analysis users use this skill to collect Jiuyan Gongshe market movement page content and generate Chinese daily briefs for review, archiving, and external delivery. The brief highlights market conditions, opportunity themes, risks, hot sectors, and leading stocks, and it includes a disclaimer that the content is not investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports hardcoded external publishing credentials and a fixed QQ recipient.

Mitigation: Replace or remove bundled credentials and recipient values before use, and confirm any external delivery destination explicitly.

Risk: The skill includes scheduled delivery instructions for daily execution.

Mitigation: Review the schedule, timeout, and delivery configuration before enabling automation.

Risk: The skill browses an external market data page and generates market commentary.

Mitigation: Use it only for the intended Jiuyan market brief workflow and retain the included disclaimer that outputs are not investment advice.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ajian11/skills/jiuyan-yidong-market)
- [Publisher profile](https://clawhub.ai/user/ajian11)
- [Jiuyan Gongshe market movement page](https://www.jiuyangongshe.com/action)
- [Market brief template](artifact/templates/market-brief-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese Markdown brief for IMA notes and Chinese plain text for QQ delivery]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces separate channel-specific formats and includes a finance disclaimer.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
