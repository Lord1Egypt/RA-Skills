## Description:

Access personal finance data from Konto, including accounts, transactions, investments, assets, loans, subscriptions, and net worth summaries via API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[angelstreet](https://clawhub.ai/user/angelstreet)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to query a configured Konto personal finance service for account balances, transactions, portfolio holdings, loans, assets, subscriptions, and financial summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Command output can expose personal financial details such as balances, transactions, subscriptions, loans, and holdings.

Mitigation: Avoid sharing command output and prefer the narrowest endpoint or filter needed for the task.

Risk: A misconfigured or untrusted Konto service URL could expose API credentials or financial data.

Mitigation: Use HTTPS, configure only trusted KONTO_URL values, and keep ~/.openclaw/secrets/konto.env private.

## Reference(s):

- [Konto API Reference](artifact/api.md)
- [Konto API on ClawHub](https://clawhub.ai/angelstreet/skills/konto-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Konto API responses that may contain sensitive personal financial data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
