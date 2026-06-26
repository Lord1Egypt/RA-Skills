## Description: <br>
Execute DEX swaps on Solana or Base, including cross-chain bridges. Use when buying or selling a token, getting a swap quote, or executing a trade. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to request Nansen CLI quotes, swaps, cross-chain bridges, bridge status checks, and Solana limit-order actions on supported chains. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-directed trading can execute irreversible on-chain swaps, bridges, and limit-order mutations. <br>
Mitigation: Require explicit user approval before execute, bridge, cancel, update, or limit-order create actions, and manually verify quotes, tokens, chains, amounts, and destination wallets. <br>
Risk: Wallet access and sensitive credentials are required, including NANSEN_API_KEY and NANSEN_WALLET_PASSWORD. <br>
Mitigation: Use a dedicated low-balance wallet, avoid broad wallet permissions, and protect any persisted wallet-password file with strict local access controls. <br>
Risk: The server security verdict is suspicious because the skill combines high-impact wallet authority with direct trade execution patterns. <br>
Mitigation: Review the skill and Nansen CLI installation before deployment, and limit use to controlled trading workflows with clear user confirmation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-trading) <br>
- [Nansen CLI npm package](https://www.npmjs.com/package/nansen-cli) <br>
- [Nansen CLI GitHub repository](https://github.com/nansen-ai/nansen-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces Nansen CLI trading commands and operational guidance for quote, execute, bridge-status, and limit-order workflows.] <br>

## Skill Version(s): <br>
0.1.5 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
