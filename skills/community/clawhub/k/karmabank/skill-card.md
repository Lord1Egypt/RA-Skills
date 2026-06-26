## Description: <br>
AI agents borrow USDC based on their Moltbook karma score. Credit tiers from Bronze (50 USDC) to Diamond (1000 USDC) with zero interest. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abdhilabs](https://clawhub.ai/user/abdhilabs) <br>

### License/Terms of Use: <br>
ISC <br>


## Use Case: <br>
External agents and KarmaBank administrators use this skill to register Moltbook identities, check karma-based credit limits, borrow and repay testnet USDC, inspect loan history, and manage Circle wallet operations for a lending pool. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can be connected to Circle credentials or funded wallets, and the security review flags weak safeguards around wallet funds. <br>
Mitigation: Review before installing, start with mock mode or isolated testnet accounts, and do not connect production-funded wallets until failed transfers fail closed and admin operations are authorized and audited. <br>
Risk: Loan records and CLI output may expose sensitive local lending or wallet activity. <br>
Mitigation: Treat local ledger files and command output as sensitive, restrict file access, and avoid sharing logs that contain account, wallet, or balance details. <br>
Risk: The security guidance says the skill should not be relied on for production lending until repayment and transfer controls are strengthened. <br>
Mitigation: Reconcile repayments, verify transfer failure behavior, and clearly separate demo or testnet behavior from any real-money deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abdhilabs/karmabank) <br>
- [Project homepage](https://github.com/openclaw/agent-credit-system) <br>
- [Moltbook](https://moltbook.com) <br>
- [Circle Console](https://console.circle.com) <br>
- [USDC Hackathon](https://moltbook.com/m/usdc) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with CLI commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command guidance for KarmaBank registration, credit checks, borrowing, repayment, history, and wallet operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
