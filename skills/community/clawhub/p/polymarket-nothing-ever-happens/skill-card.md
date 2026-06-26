## Description: <br>
Scans standalone non-sports yes/no Polymarket markets, filters by price, liquidity, fees, and safeguards, and can buy NO shares through the Simmer SDK. <br>

This skill is for demonstration purposes and not for production usage. <br>

## Publisher: <br>
[simmer](https://clawhub.ai/user/simmer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and prediction-market operators use this skill to evaluate or run a configurable NO-buying strategy for selected Polymarket markets. It supports scanning, dry-run review, configuration changes, and live execution when the operator provides credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real-money trades and handles wallet authority. <br>
Mitigation: Review before installing, use only a dedicated low-balance wallet, avoid providing a primary wallet private key, and test dry-run behavior before live execution. <br>
Risk: Startup may redeem existing winning positions automatically without clear enough user control. <br>
Mitigation: Make redemption explicit during review and require operator acknowledgement before live use. <br>
Risk: The security verdict is suspicious because live trading behavior and credential risks are not warned about strongly enough. <br>
Mitigation: Add stronger private-key and real-money warnings before deployment, and assume --live can place real trades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simmer/polymarket-nothing-ever-happens) <br>
- [Original nothing-ever-happens strategy](https://github.com/sterlingcrispin/nothing-ever-happens) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with bash commands; runtime output is terminal text and optional JSON status.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May place real trades only when run with --live and valid credentials.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
