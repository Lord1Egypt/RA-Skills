## Description:

KIS Trading uses the Korea Investment & Securities Open API for Korean stock account balances, quotes, buy and sell orders, trade history, holdings, and market overview.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tgparkk](https://clawhub.ai/user/tgparkk)

### License/Terms of Use:


## Use Case:

External users and developers can use this skill to connect an agent to Korea Investment & Securities Open API workflows for KRX stock account review, quotes, holdings, market summaries, trade history, and user-confirmed buy or sell orders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can submit live Korean stock orders through KIS APIs and may affect a real brokerage account.

Mitigation: Use virtual trading first and require explicit confirmation of the account, environment, side, stock code, quantity, price, and order type before running scripts/order.py without --dry-run.

Risk: The skill handles KIS app keys, app secrets, account numbers, and access tokens.

Mitigation: Keep credentials in local configuration, avoid exposing logs or transcripts, protect token files, and rotate credentials if they are disclosed.

Risk: An incorrect or untrusted KIS_BASE_URL could send credentials or orders to an unintended endpoint.

Mitigation: Validate KIS_BASE_URL against the official KIS live or virtual trading endpoints before use.

## Reference(s):

- [KIS Open API endpoint reference](references/kis-api-guide.md)
- [ClawHub skill page](https://clawhub.ai/tgparkk/skills/kis-trading)
- [KIS live API endpoint](https://openapi.koreainvestment.com:9443)
- [KIS virtual trading API endpoint](https://openapivts.koreainvestment.com:29443)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Console text and Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include account balances, holdings, quote data, order confirmations, trade history, market summaries, and setup checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
