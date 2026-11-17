## Description: <br>
jinn-node-free guides an agent through configuring and running a free Jinn worker node for a single on-chain task, including wallet balance checks on Base. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure a Jinn node, fund and stake its wallet, run a single worker test, and check ETH/OLAS balances before considering a full node deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to run a funded blockchain-node workflow with local secrets and broad agent authority. <br>
Mitigation: Review the skill before installing or invoking it, use a dedicated workspace, verify the repository and commands before setup, and use least-privilege API keys. <br>
Risk: Wallet funding, staking, local .env values, and .operate state can expose funds or secrets if mishandled. <br>
Mitigation: Keep .env and .operate out of version control and prompts, and do not fund or stake more ETH/OLAS than you are prepared to lock until withdrawal and recovery paths are independently confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/jinn-node-free) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration variables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local command execution, network access, API credentials, and funded ETH/OLAS wallet state.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
