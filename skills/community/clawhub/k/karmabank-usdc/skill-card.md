## Description: <br>
AI agents borrow USDC based on their Moltbook karma score, with credit tiers from Bronze to Diamond and zero interest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abdhilabs](https://clawhub.ai/user/abdhilabs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and agent operators use KarmaBank to register agents, check reputation-based credit limits, and prepare USDC borrowing, repayment, wallet, and transaction-history commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes financial actions and asks for real wallet credentials without enough reviewed implementation detail. <br>
Mitigation: Review the full CLI implementation and local Circle wallet dependency before running it. <br>
Risk: Wallet creation, borrowing, repayment, or other fund-moving operations could affect assets or test assets. <br>
Mitigation: Use isolated test or sandbox credentials only, require explicit human confirmation, and set spending limits for any wallet or fund-moving operation. <br>


## Reference(s): <br>
- [KarmaBank ClawHub page](https://clawhub.ai/abdhilabs/karmabank-usdc) <br>
- [Moltbook](https://moltbook.com) <br>
- [Circle Console](https://console.circle.com) <br>
- [USDC Agentic Hackathon](https://moltbook.com/m/usdc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and configuration variables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require Moltbook and Circle API credentials for full operation.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.json release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
