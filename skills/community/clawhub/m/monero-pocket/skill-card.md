## Description: <br>
Ripley Pocket For Monero helps agents use the Ripley Pocket API to register accounts, check XMR balances, send agent payments, withdraw Monero, perform cross-chain swaps, and handle XMR402 payment challenges. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xbtoshi](https://clawhub.ai/user/xbtoshi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to connect AI agents to Ripley Pocket for custodial Monero balances, agent-to-agent payments, withdrawals, deposits, swaps, and XMR402 payment flows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can initiate payments, withdrawals, swaps, deposits, or XMR402 payments with broad funds-moving authority. <br>
Mitigation: Use a dedicated low-balance account and require manual confirmation of recipient, amount, network, fees, and irreversibility before every funds-moving call. <br>
Risk: The API key controls account access and payment capability. <br>
Mitigation: Protect and rotate the API key; avoid exposing it in prompts, logs, generated code, or shared transcripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xbtoshi/monero-pocket) <br>
- [Ripley Pocket API gateway](https://pocket.ripley.run) <br>
- [XMR402 protocol](https://xmr402.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with REST API examples, curl commands, and Python or TypeScript snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an API_KEY credential and uses RIPLEY_URL, defaulting to https://pocket.ripley.run.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
