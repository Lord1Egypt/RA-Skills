## Description: <br>
AgentWallet is a secure multi-chain wallet skill for AI agents that creates wallets, checks balances, and signs or broadcasts transactions across EVM chains, Solana, and TON while keeping private keys in the vault process. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Phlegonlabs](https://clawhub.ai/user/Phlegonlabs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and operators use AgentWallet to let an AI agent manage multi-chain wallet workflows through the agentwallet CLI, including wallet creation, balance checks, transaction signing, x402 payment signing, and token transfers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable an AI agent to sign or send real blockchain payments without clear per-transaction approval safeguards. <br>
Mitigation: Require explicit user approval for every transfer or signature, verify the npm package and source before use, and keep funds limited and segregated. <br>
Risk: Unlocked wallet sessions or retained tokens can authorize wallet operations beyond the intended action. <br>
Mitigation: Use short unlock sessions, pass session tokens instead of passwords, store tokens only as needed for the current task, and lock the wallet immediately afterward. <br>


## Reference(s): <br>
- [AgentWallet ClawHub page](https://clawhub.ai/Phlegonlabs/phlegon-agentwallet) <br>
- [AgentWallet repository link from metadata](https://github.com/user/agentwallet) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI-oriented guidance for JSON output, session tokens, wallet operations, transaction signing, and transfer execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
