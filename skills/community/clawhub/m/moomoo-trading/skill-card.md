## Description: <br>
Use OpenD-backed moomoo/Futu scripts for quotes, K-lines, price alerts, portfolio/account checks, and stock order execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bobbythebot2008-beep](https://clawhub.ai/user/bobbythebot2008-beep) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading automation users use this skill to operate moomoo/Futu OpenD workflows for market data, simulated trading, portfolio review, and explicitly confirmed live stock orders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live trading can place, modify, or cancel real-money stock orders when a user explicitly selects the real environment. <br>
Mitigation: Keep simulated mode for routine use, and require users to verify ticker, quantity, price, market, account, --env real, and --confirm before live order actions. <br>
Risk: The live-trading unlock password is sensitive and enables account mutation through OpenD. <br>
Mitigation: Expose MOOMOO_UNLOCK_PASSWORD only in sessions where live trading is needed, and never place the raw trading password directly on a command line. <br>
Risk: Incorrect market, account, entitlement, or OpenD connection state can cause failed or unintended trading and portfolio actions. <br>
Mitigation: Run the setup check, confirm OpenD login and permissions, and use explicit market or account selectors before acting on orders or account data. <br>


## Reference(s): <br>
- [API Reference](references/api-reference.md) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Futu OpenAPI Documentation](https://openapi.futunn.com/futu-api-doc/en/) <br>
- [moomoo OpenAPI Documentation](https://openapi.moomoo.com/moomoo-api-doc/en/) <br>
- [moomoo OpenAPI Download](https://www.moomoo.com/download/OpenAPI) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces OpenD-backed command guidance and script output; live trading requires explicit confirmation and an unlock password environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
