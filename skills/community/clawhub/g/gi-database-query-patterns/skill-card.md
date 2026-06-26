## Description: <br>
Write database queries using tkms AsyncSqlSessionTemplate for DAO-layer SQL, including insert, update, single-row, and list queries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[laimiaohua](https://clawhub.ai/user/laimiaohua) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement database access patterns with tkms AsyncSqlSessionTemplate, parameterized MySQL queries, DAO methods, pagination, counts, table definitions, indexes, and transaction guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SQL or DAO code may change production data or schema if applied without review. <br>
Mitigation: Review generated inserts, updates, schema changes, and transaction logic before applying them to real systems. <br>
Risk: Database queries may be incorrect for the target schema, indexes, or transaction requirements. <br>
Mitigation: Validate generated queries against the project schema and test expected results, pagination, counts, and rollback behavior before deployment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Markdown with Python and SQL code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; generated SQL and DAO code should be reviewed before use against real databases.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
