## Description:

Real-time stock quotes and account queries for Longbridge users, including US, Hong Kong, and China A-share market quotes, account balance, and portfolio positions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weipapa](https://clawhub.ai/user/weipapa)

### License/Terms of Use:

MIT-0

## Use Case:

External Longbridge users and developers use this skill to retrieve stock quotes, account balances, and portfolio positions through Longbridge API scripts. It is suited for market lookup and account review workflows where the user intentionally provides Longbridge credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles brokerage credentials and account data.

Mitigation: Install only when the agent is intended to use Longbridge credentials, prefer a dedicated low-privilege token if available, and ask for confirmation before balance or position queries.

Risk: The configuration can store credentials in plaintext files.

Mitigation: Store the config outside shared workspaces with restrictive file permissions and do not commit it.

Risk: Custom Longbridge API endpoints can redirect sensitive API traffic.

Mitigation: Use the documented Longbridge endpoints unless the custom endpoint is fully trusted.

## Reference(s):

- [Longbridge API configuration](references/config.md)
- [Stock symbol formats](references/symbols.md)
- [Longbridge Open Platform](https://open.longport.com/)
- [ClawHub skill page](https://clawhub.ai/weipapa/skills/longbridge-stock)
- [Publisher profile](https://clawhub.ai/user/weipapa)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and console text with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include real-time market data and account data returned by the Longbridge API.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
