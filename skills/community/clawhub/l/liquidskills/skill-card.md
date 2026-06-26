## Description: <br>
Liquidskills is a Hyperliquid development knowledge base for agents building production dApps, covering HyperCore, HyperEVM, APIs, wallets, gas, security, testing, deployment, and review workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudzombie](https://clawhub.ai/user/cloudzombie) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI coding agents use this skill to plan, implement, secure, test, deploy, and review Hyperliquid dApps and integrations. It helps route work across HyperCore and HyperEVM topics such as APIs, asset IDs, nonces, signing, wallet setup, frontend UX, indexing, and audit checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Examples involving orders, transfers, withdrawals, bridge actions, deployments, or forge and cast broadcasts can affect real funds if copied or automated. <br>
Mitigation: Use testnet first, require explicit human approval before mainnet actions, and treat transaction examples as proposals until reviewed. <br>
Risk: Main wallet keys or broad signing authority could expose funds if delegated to an agent. <br>
Mitigation: Use limited API wallets, never provide a main wallet private key to an agent, and scope permissions to the smallest practical account or wallet. <br>
Risk: Incorrect bridge direction, asset IDs, token decimals, or contract addresses can route actions to the wrong place or cause permanent loss. <br>
Mitigation: Verify bridge direction, asset metadata, decimals, and contract addresses against official sources and block explorers before execution. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/cloudzombie/liquidskills) <br>
- [Hyperliquid Docs](https://hyperliquid.gitbook.io/hyperliquid-docs/) <br>
- [Hyperliquid Python SDK](https://github.com/hyperliquid-dex/hyperliquid-python-sdk) <br>
- [Hyperliquid TypeScript SDK](https://github.com/nktkas/hyperliquid) <br>
- [HyperEVM Explorer](https://explorer.hyperliquid.xyz) <br>
- [Liquidskills Root Guide](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline code blocks, command examples, configuration snippets, and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Topic-specific guidance is split across standalone SKILL.md files and should be applied with human review before transactions, deployments, or security decisions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
