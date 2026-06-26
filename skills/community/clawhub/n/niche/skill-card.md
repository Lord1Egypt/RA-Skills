## Description: <br>
Trading card marketplace with partial USDC deposits. Browse cards, deposit partial amounts, and complete purchases with secure on-chain escrow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ClementSutjiatma](https://clawhub.ai/user/ClementSutjiatma) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and their agents use this skill to browse, list, watch, and transact peer-to-peer trading cards with partial USDC deposits and in-person inspection before final payment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can initiate wallet, escrow, payment, refund, funding, dispute, and scheduled background actions through an unreviewed external CLI. <br>
Mitigation: Require explicit user approval before login, browser transaction flows, listing changes, deposits, confirmations, cancellations, refunds, funding, disputes, or scheduled match checks. <br>
Risk: Credential handling, backend ownership, and cron behavior are not verified by the available evidence. <br>
Mitigation: Use only testnet or disposable accounts until the CLI source, backend ownership, credential handling, and scheduled behavior have been independently verified. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/ClementSutjiatma/niche) <br>
- [Publisher profile](https://clawhub.ai/user/ClementSutjiatma) <br>
- [Hosted UI](https://niche-ddq89ltdk-clement-sutjiatmas-projects.vercel.app) <br>
- [Circle USDC faucet](https://faucet.circle.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and concise user-facing guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May open hosted browser flows for login, deposits, confirmations, funding, browsing, and card detail views.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
