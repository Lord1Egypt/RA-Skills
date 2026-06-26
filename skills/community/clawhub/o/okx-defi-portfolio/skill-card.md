## Description: <br>
Okx Defi Portfolio helps agents view DeFi positions and per-protocol holdings across supported chains without handling deposit, redeem, claim, wallet balance, or swap operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ok-james-01](https://clawhub.ai/user/ok-james-01) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect wallet DeFi holdings, staking positions, lending positions, and protocol-level position details across supported chains through onchainos commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The all-wallets flow can switch active wallet accounts without a documented restore or confirmation step. <br>
Mitigation: Prefer a manually supplied public address when possible, and after any all-wallets query confirm which wallet account is active before making transactions. <br>


## Reference(s): <br>
- [OKX Web3](https://web3.okx.com) <br>
- [ClawHub Skill Page](https://clawhub.ai/ok-james-01/okx-defi-portfolio) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown tables with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes wallet address, chain, platform-id, investment-id, and account-selection guidance.] <br>

## Skill Version(s): <br>
3.1.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
