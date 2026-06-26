## Description: <br>
Trade Agent helps a personal assistant manage AIUSD account workflows such as balance checks, trading, staking, withdrawals, gas top-ups, and transaction history through authenticated tool calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freeman88-tch](https://clawhub.ai/user/freeman88-tch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and bot operators use this skill to manage AIUSD trading-account workflows from chat, including checking balances, executing trades or swaps, staking or unstaking, withdrawing funds, topping up gas, and reviewing transactions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access an AIUSD account and may trade, stake, withdraw, or top up gas. <br>
Mitigation: Install only when these account actions are intended, and require manual confirmation of asset, amount, destination, chain, fees, and slippage before funds move. <br>
Risk: Automatic installer and authentication flows can affect a local bot environment and credentials. <br>
Mitigation: Use a trusted private device and bot session, inspect or sandbox the installer before running it, and back up any existing aiusd-skill directory. <br>
Risk: Security evidence marks the release suspicious because it appears to be a real trading skill with fund-moving capabilities. <br>
Mitigation: Review the skill and its requested permissions before deployment, and avoid using it with accounts or wallets that should not be exposed to automated trading actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/freeman88-tch/lobster-trade-agent) <br>
- [AIUSD Website](https://aiusd.ai) <br>
- [AIUSD Skill Release Download](https://github.com/galpha-ai/aiusd-skills/releases/download/v1.0.0/aiusd-skill-agent.skill) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API calls, Configuration, Guidance] <br>
**Output Format:** [Markdown or plain text with shell commands and tool-call parameters when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires authenticated AIUSD account access; agents should confirm asset, amount, destination, chain, fees, and slippage before any transaction moves funds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release, SKILL.md frontmatter, build-info.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
