## Description: <br>
Deploy tokens on Solana, trade on pump.fun and Jupiter, and earn creator fees. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[SerPepe](https://clawhub.ai/user/SerPepe) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Agents and developers use this skill to set up P0 API access, create and deploy Solana token projects, trade tokens, monitor positions, manage fees, and handle P0 account operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable live crypto trading, token deployment, purchasing, fee claiming, account upgrades, batch actions, and API key revocation. <br>
Mitigation: Require manual approval for every deploy, swap, fee claim, purchase, upgrade, batch action, and key revocation. <br>
Risk: A compromised or over-permissioned P0 API key could expose funds or account controls. <br>
Mitigation: Store P0_API_KEY only in environment or secret storage, use a dedicated low-balance wallet or account, and rotate or revoke keys when access is no longer needed. <br>
Risk: Unbounded spending or market execution can create financial loss through token deployments, swaps, slippage, or credit purchases. <br>
Mitigation: Set strict spending, balance, and slippage limits before allowing the agent to call P0 trading or account-management endpoints. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/SerPepe/p0-systems) <br>
- [P0 agents documentation](https://agents.p0.systems) <br>
- [P0 hosted skill documentation](https://agents.p0.systems/skill.md) <br>
- [P0 website](https://p0.systems) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with API examples and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires P0_API_KEY for authenticated P0 API operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
