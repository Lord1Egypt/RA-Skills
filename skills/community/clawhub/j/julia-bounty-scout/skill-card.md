## Description: <br>
Autonomous GitHub and multi-platform bounty hunter that scans for high-value issues, filters by skills and ROI, drafts proposals and PRs, and tracks payments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronmda](https://clawhub.ai/user/aaronmda) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agents use Julia Bounty Scout to find bounty opportunities, prioritize them by reward and skill fit, draft proposals or PRs, and track submissions and payments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unattended bounty submissions or PRs can create inaccurate, spammy, or unauthorized platform activity. <br>
Mitigation: Require explicit approval for every outbound proposal, PR, or platform interaction before submission. <br>
Risk: Wallets and sensitive account credentials can expose payment or account access if connected without clear boundaries. <br>
Mitigation: Use least-privilege credentials and do not connect wallets or sensitive accounts unless the skill clearly documents what it can read and write. <br>
Risk: Background runs can create repeated outbound activity without enough user oversight. <br>
Mitigation: Avoid unattended operation unless strict rate limits, activity logs, and stop controls are configured. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaronmda/julia-bounty-scout) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with proposal drafts, issue analysis, PR or code suggestions, and tracking notes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May involve outbound platform interactions and wallet or payment tracking when connected to accounts.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
