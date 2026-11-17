## Description:

Provides paid birthday-themed readings from Juhe Data based on a user-supplied date, returning birthday book, birthday code, flower-language, personality, fortune, and related entertainment content after Alipay payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juhemcp](https://clawhub.ai/user/juhemcp)

### License/Terms of Use:

MIT-0

## Use Case:

External users can request entertainment-only birthday readings for a specific date. The agent confirms paid service terms, sends only the requested date to Juhe Data, routes payment through Alipay, and formats the returned result as structured Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment setup may ask the agent to install and enable Alipay payment support with an unpinned @latest npm command.

Mitigation: Review and pin the Alipay package source and version in an isolated environment before enabling payment capability.

Risk: The paid lookup sends the user's requested birth date to Juhe Data.

Mitigation: Ask for explicit consent before collecting the date, send only the date required for the lookup, and avoid requesting phone numbers, identity numbers, addresses, or unrelated personal data.

Risk: Birthday and fortune-style results may be mistaken for factual prediction or professional advice.

Mitigation: Present the result as entertainment-only content and avoid using it for health, career, relationship, financial, or other consequential decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juhemcp/skills/juhe-birthday-oracle-a2a)
- [Juhe A2A query endpoint](https://apis.juhe.cn/a2a/query)
- [Output format](artifact/OUT_FORMAT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Structured Markdown with tables and lists, plus inline shell command examples for API calls.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a specific date and user payment confirmation before querying; paid results should use only fields returned by the Juhe API.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
