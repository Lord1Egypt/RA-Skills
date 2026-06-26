## Description: <br>
Personal finance management skill for tracking expenses, analyzing budgets, monitoring net worth, and managing finances through a self-hosted Maybe Finance instance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[antonia-sz](https://clawhub.ai/user/antonia-sz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage personal finance workflows in a self-hosted Maybe Finance environment, including account review, transaction tracking, budget analysis, net worth snapshots, and cash-flow reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for Maybe Finance API access while the included CLI mostly shows hardcoded demo data and can report successful actions without actually updating Maybe Finance. <br>
Mitigation: Treat the API token as a secret, use only a trusted self-hosted Maybe instance, and verify balances, reports, and transaction changes directly in Maybe before relying on them. <br>
Risk: Account update or delete workflows may affect financial records if connected to a live Maybe Finance instance. <br>
Mitigation: Review account-changing commands before execution and keep backups of financial data. <br>


## Reference(s): <br>
- [Maybe Finance OS](https://github.com/maybe-finance/maybe) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, environment variable examples, and CLI output guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include finance CLI commands and JSON export guidance; users should verify live Maybe Finance results before relying on balances or write confirmations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
