## Description:

Connect bank accounts to AI models using openfinance.sh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[winxton](https://clawhub.ai/user/winxton)

### License/Terms of Use:

MIT-0

## Use Case:

People with connected OpenFinance accounts can use an agent to review balances and transactions, analyze spending, and create account reconnect links when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Access to sensitive account balances and transaction history.

Mitigation: Install only when such access is intended; request only the fields and date ranges needed.

Risk: Exposure of API credentials, financial responses, or account reconnect links.

Mitigation: Keep the API key private and do not post reconnect links or financial responses in shared chats or logs.

## Reference(s):

- [openfinance on ClawHub](https://clawhub.ai/winxton/skills/openfinance)
- [OpenFinance](https://openfinance.sh)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Text or Markdown with shell commands and financial summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contain sensitive account balances, transaction details, and account reconnect links.]

## Skill Version(s):

0.0.4 (source: frontmatter and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
