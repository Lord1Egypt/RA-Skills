## Description: <br>
Helps agents search and read YNAB budget data through OOMOL's oo connector instead of calling the YNAB API directly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to retrieve YNAB user, plan, account, category, month, payee, and transaction information from an OOMOL-connected YNAB account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: YNAB budgets and transactions can contain sensitive financial data. <br>
Mitigation: Install only when OOMOL connector access to YNAB data is acceptable, and treat connector outputs as sensitive. <br>
Risk: Generated oo commands may access or expose more YNAB data than intended if the action or payload is wrong. <br>
Mitigation: Review generated oo commands and fetch the live connector schema before constructing each payload. <br>
Risk: Future connector actions could change or delete YNAB data. <br>
Mitigation: Require explicit user confirmation before any write or destructive action if such actions become available. <br>


## Reference(s): <br>
- [ClawHub YNAB Skill](https://clawhub.ai/oomol/oo-ynab) <br>
- [YNAB](https://www.ynab.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [OOMOL CLI Install Guide](https://cli.oomol.com/install-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, JSON, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the oo CLI, OOMOL sign-in, and an OOMOL-connected YNAB account.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
