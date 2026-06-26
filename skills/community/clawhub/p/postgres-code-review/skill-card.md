## Description: <br>
Reviews PostgreSQL code for indexing strategies, JSONB operations, connection pooling, and transaction safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to review PostgreSQL queries, schemas, JSONB usage, connection management, and transaction behavior before reporting evidence-based findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Example SQL and Python snippets may be unsuitable if copied directly into a production schema, especially examples involving account updates, locks, timeouts, or placeholder credentials. <br>
Mitigation: Adapt examples to the application's schema, transaction model, credential handling, and operational limits before use. <br>
Risk: Review findings can be misleading if performance, JSONB, transaction, connection, or SQL injection claims are made without code evidence. <br>
Mitigation: Require concrete file, line, symbol, SQL, DDL, or binding-mechanism citations before reporting conclusions. <br>


## Reference(s): <br>
- [PostgreSQL index review reference](references/indexes.md) <br>
- [PostgreSQL JSONB review reference](references/jsonb.md) <br>
- [PostgreSQL connection review reference](references/connections.md) <br>
- [PostgreSQL transaction review reference](references/transactions.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Guidance] <br>
**Output Format:** [Markdown review findings with cited code locations and SQL or Python examples when relevant] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Findings should cite reviewed paths or statements before making performance, JSONB, transaction, connection, or SQL injection claims.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
