## Description: <br>
Audits KA rebate workbooks by identifying monthly worksheet structures, recalculating rebates from source records, comparing results with summary sheets, and producing structured audit reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[runkecheng](https://clawhub.ai/user/runkecheng) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Internal audit and finance employees use this skill to check KA rebate calculations, reconcile monthly workbooks against independently recalculated totals, and generate management and detailed audit reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bundled database rebuild, reparse, restore, and analysis scripts can overwrite or delete audit database history. <br>
Mitigation: Require backups and explicit user approval before running scripts that can DELETE, DROP, UPDATE, rebuild, reparse, or restore SQLite data. <br>
Risk: Audit data and reports may expose sensitive payout, bank account, account-holder, or email information. <br>
Mitigation: Store reports and databases only in approved business locations and mask sensitive fields in terminal logs and shared reports where possible. <br>
Risk: Incorrect worksheet classification or formula assumptions can produce misleading audit conclusions. <br>
Mitigation: Ask the user to classify unknown sheets and verify generated Word and Excel reports against the source workbooks before business use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/runkecheng/nk-ka-fy-audit) <br>
- [Structure variants reference](references/01-structure-variants.md) <br>
- [Recalculation methodology](references/02-recalculation-methodology.md) <br>
- [Abnormal rules reference](references/03-abnormal-rules.md) <br>
- [Database schema and incremental import flow](references/04-database-schema.md) <br>
- [Historical errors review](references/05-historical-errors.md) <br>
- [Operating norms](references/06-operating-norms.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated Word and Excel audit files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should be reviewed against source workbooks and business rules before relying on audit conclusions.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
