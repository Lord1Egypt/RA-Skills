## Description: <br>
Set up automated trading on Polymarket, including wallet setup, token approvals, API authentication, market discovery, order placement, WebSocket feeds, and position management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[emsin44](https://clawhub.ai/user/emsin44) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and trading-system builders use this skill to configure a Polymarket automation environment, derive and store credentials, connect to Polymarket API surfaces, and validate order-placement flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks an agent to handle financial keys and Polymarket API secrets. <br>
Mitigation: Use a dedicated, limited-funds wallet; keep .env files out of source control with restrictive permissions; never paste private keys or API secrets into chats or logs; and rotate or revoke credentials if exposure is possible. <br>
Risk: The setup includes token approvals and real order submission on a prediction market. <br>
Mitigation: Require explicit approval before any token approval or order submission, prefer bounded USDC approvals, and use a far-from-market test order only after the user confirms the target market and amount. <br>


## Reference(s): <br>
- [Polymarket Trading API Guide](artifact/GUIDE.md) <br>
- [Polymarket CLOB Python client](https://github.com/Polymarket/py-clob-client) <br>
- [ClawHub skill page](https://clawhub.ai/emsin44/polymarket-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash, Python, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Polymarket wallet and API environment variables, including private key and CLOB API credentials; optional Builder API credentials are used for headless approvals.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
