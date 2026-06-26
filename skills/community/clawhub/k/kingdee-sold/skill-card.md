## Description: <br>
金蝶EAS Cloud ERP系统数据库SQL查询技能，支持采购、销售、库存、财务等模块的单据查询和数据分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fxy-99](https://clawhub.ai/user/fxy-99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ERP analysts, developers, and operations staff use this skill to draft and run read-oriented PostgreSQL queries for Kingdee EAS Cloud ERP documents, including sales orders, purchase orders, inventory, accounts payable, accounts receivable, and finance records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports embedded reusable database credentials. <br>
Mitigation: Do not install or use the skill until the publisher removes the credentials, the exposed account is rotated, and database access logs are reviewed. <br>
Risk: The security review reports broad discovery queries against ERP data. <br>
Mitigation: Limit use to approved business queries with read-only credentials, explicit date filters, and row limits before running against production data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fxy-99/kingdee-sold) <br>
- [Kingdee ERP common table list](references/tables.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown with SQL and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include database query results serialized as JSON when using the bundled query helper.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
