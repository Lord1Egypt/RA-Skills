## Description:

A standardized adapter gateway skill exclusively for OKX exchange to execute trading actions (buy/sell) and query capabilities across OKX Live and Demo environments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iceonme](https://clawhub.ai/user/iceonme)

### License/Terms of Use:


## Use Case:

Developers and trading agents use this skill to query OKX account balances, positions, and recent trades, and to submit market or limit buy/sell orders through OKX demo or live environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place live OKX financial orders with weak built-in safeguards.

Mitigation: Use demo mode by default, require explicit approval before live trading, and add order-size limits before delegating live order placement to an agent.

Risk: The skill depends on OKX credentials that may be stored in a local plaintext .env file.

Mitigation: Restrict API keys to minimum required permissions, disable withdrawals, use IP allowlisting when available, and avoid packaging real credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/iceonme/skills/okx-trading-exe)
- [Publisher profile](https://clawhub.ai/user/iceonme)
- [OKX](https://www.okx.com)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [JSON responses and stdout text from command-line execution]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OKX API credentials in environment variables or a local .env file before API calls can run.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
