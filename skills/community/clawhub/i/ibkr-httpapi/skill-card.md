## Description:

Connect to a user-run ibkr-httpapi service to retrieve IBKR market data and account information, run technical analysis, and manage orders with per-action confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and traders who have deployed ibkr-httpapi use this skill to retrieve market data, inspect accounts and positions, and run technical analysis. Order placement, cancellation, and option exercise require explicit confirmation for each action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Order placement, cancellation, and option exercise can affect a real brokerage account.

Mitigation: Confirm the target account and endpoint, review the resolved action and parameters, and obtain explicit user confirmation for each account-changing request.

Risk: An unset API token leaves the service unauthenticated to anyone who can reach it.

Mitigation: Configure bearer-token authentication and keep the service on loopback or behind a trusted authenticated connection.

Risk: The security scan was partial and its evidence is incomplete.

Mitigation: Treat the benign verdict as limited evidence and review the unresolved references and unscanned components before deployment.

## Reference(s):

- [Setup guide](references/setup.md)
- [Project documentation (skill-declared homepage)](https://github.com/psyb0t/ibkr-httpapi)
- [ib_async](https://github.com/ib-api-reloaded/ib_async)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [OpenClaw plugin](https://github.com/psyb0t/ibkr-httpapi/tree/main/.agents/plugins/ibkr-httpapi)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Text and JSON, with shell commands when invoking the service]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected IBKR account, endpoint configuration, and available market data.]

## Skill Version(s):

0.5.8 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
