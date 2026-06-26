## Description: <br>
Applies a China interbank CNY funding trader workflow for money-market analysis, repo funding and placement decisions, liquidity management, collateral eligibility checks, counterparty communication, risk checks, and post-trade review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hjh5555](https://clawhub.ai/user/hjh5555) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and financial-market operators use this skill as decision support for CNY interbank funding and pledged-repo workflows, including funding plans, trader-style notes, collateral checks, counterparty wording, and post-trade reviews. It is not trade authorization, legal advice, compliance approval, or a substitute for approved institutional systems. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Outputs could be mistaken for trade authorization or binding investment, legal, regulatory, or compliance advice. <br>
Mitigation: Treat outputs as decision support only and require a qualified human trader, risk, settlement, or compliance reviewer to approve real actions. <br>
Risk: Market prices, funding levels, account limits, collateral eligibility, and settlement status may be stale, incomplete, or absent. <br>
Mitigation: Verify all live prices, account rules, collateral records, counterparty limits, and settlement steps in approved institutional systems before execution. <br>
Risk: Template collateral files and the default account path can produce example-scope results if used without replacement. <br>
Mitigation: Replace template CSV/TSV files with approved production data and explicitly confirm the real account before relying on collateral-check output. <br>
Risk: Pasted account, counterparty, token, or position data could expose confidential information in shared prompts or templates. <br>
Mitigation: Sanitize sensitive data before use and avoid placing confidential identifiers, tokens, or non-public positions into shared artifacts. <br>


## Reference(s): <br>
- [Market Map](references/01-market-map.md) <br>
- [Decision Playbook](references/02-decision-playbook.md) <br>
- [Data Inputs](references/03-data-inputs.md) <br>
- [Risk Controls](references/04-risk-controls.md) <br>
- [Communication Style](references/05-communication-style.md) <br>
- [Case Library](references/06-case-library.md) <br>
- [Review and Learning](references/07-review-and-learning.md) <br>
- [Collateral Verification](references/08-collateral-verification.md) <br>
- [iFinD Finance Data Skill](references/09-ifind-finance-data-skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, tables, communication drafts, review notes, and optional TSV-style collateral-check output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local templates and a collateral verification script; outputs require human review before trading, settlement, or compliance use.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
