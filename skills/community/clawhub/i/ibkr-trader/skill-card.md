## Description:

Automates Interactive Brokers (IBKR) account authentication, portfolio checks, market data access, and order workflows through the Client Portal API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flokiew](https://clawhub.ai/user/flokiew)

### License/Terms of Use:


## Use Case:

Developers, engineers, and trading operators use this skill to set up IBKR Client Portal access, maintain authenticated sessions, inspect accounts and positions, and build IBKR trading automation. It is most appropriate in a dedicated trusted environment with paper trading and human order review before any live brokerage use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live brokerage automation can place or confirm real orders.

Mitigation: Use a paper IBKR account first, require explicit human approval for each order confirmation, and enforce account, symbol, quantity, and notional limits before any live trading.

Risk: Credential handling relies on a plaintext .env flow.

Mitigation: Use a dedicated trusted host, protect local credential files, avoid committing secrets, and replace the plaintext flow with a secrets manager or equivalent protected store where possible.

Risk: Gateway trust and dependency integrity are important because the skill downloads software and communicates with a local brokerage gateway.

Mitigation: Restrict the gateway to a verified local endpoint, limit network exposure, and pin or verify downloaded dependencies before use.

## Reference(s):

- [IBKR Client Portal API Reference](references/api-endpoints.md)
- [IBKR Client Portal Gateway Download](https://download2.interactivebrokers.com/portal/clientportal.gw.zip)
- [ClawHub Skill Page](https://clawhub.ai/flokiew/skills/ibkr-trader)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, curl, Python, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include executable setup scripts and IBKR API request payloads; outputs depend on local Client Portal Gateway authentication state.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
