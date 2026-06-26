## Description: <br>
Autonomous DeFi yield management on Giza for onboarding, portfolio reviews, withdrawals, rewards, and education across Base, Arbitrum, Plasma, and HyperEVM. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[raphaelDkhn](https://clawhub.ai/user/raphaelDkhn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to manage Giza DeFi stablecoin accounts: onboarding, reviewing balances and APR, routing account actions through Giza tools, and learning about risks and fees. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change real DeFi account state and yield strategy, including withdrawals, deposits, deactivation, and protocol changes. <br>
Mitigation: Before any withdrawal, deactivation, deposit processing, or protocol change, require the assistant to restate the exact network, amount or protocols, expected fund movement, fees, risks, and reversibility, then proceed only after explicit user approval. <br>
Risk: The security review says the skill is coherent but has some under-scoped or overly broad instructions for DeFi account automation. <br>
Mitigation: Install only if the user trusts Giza and is comfortable with DeFi account automation; verify portfolio data, APRs, protocols, and transaction details before relying on an action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/raphaelDkhn/giza) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, API Calls] <br>
**Output Format:** [Markdown-formatted conversational responses with Giza MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include financial amounts, APRs, networks, protocols, transaction status, login URLs, and confirmation prompts.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
