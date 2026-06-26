## Description: <br>
Nummo connects AI agents to the user's bank accounts via Plaid, enabling financial insights through natural language. More info at nummo.ai. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nummo-ai](https://clawhub.ai/user/nummo-ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to connect bank accounts, inspect account lists, review transactions, summarize spending and income, and manage Nummo subscription flows through the Nummo CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill provides access to Plaid-linked bank account and transaction data. <br>
Mitigation: Ask for explicit user consent before each financial-data command and avoid broad history access such as `--all` unless it is necessary for the user's request. <br>
Risk: The install path uses a remote shell installer. <br>
Mitigation: Install only after trusting Nummo with local CLI execution; inspect the installer first or prefer a signed package with checksum verification. <br>
Risk: Returned connection or payment URLs require user action outside the agent. <br>
Mitigation: Present Plaid Link and Stripe checkout URLs clearly and tell the user they must open them in a browser to continue. <br>


## Reference(s): <br>
- [Install Reference](reference/install.md) <br>
- [Nummo Installer](https://nummo.ai/install) <br>
- [Nummo Skill Page](https://clawhub.ai/nummo-ai/nummo) <br>
- [Nummo Publisher Profile](https://clawhub.ai/user/nummo-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and URLs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Plaid Link URLs, Stripe checkout URLs, account lists, transaction details, spending summaries, subscription status, and cancellation guidance.] <br>

## Skill Version(s): <br>
0.1.8 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
