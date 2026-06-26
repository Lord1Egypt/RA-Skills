## Description: <br>
Analyzes query patterns for a specified table or collection, designs reusable indexes, and validates changes through iterative EXPLAIN checks in full-table or single-query mode. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jiang-zx](https://clawhub.ai/user/jiang-zx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database engineers use this skill to inventory queries for a target table or collection, design minimal reusable indexes, validate index usage with EXPLAIN output, and prepare rollback SQL. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can propose or execute database index creation or deletion, and the artifact describes a default no-confirmation mode. <br>
Mitigation: Use confirmation-required mode, require human review before DDL or dropIndex execution, and keep rollback SQL with each proposed index change. <br>
Risk: Index changes can affect write performance, locking behavior, storage use, and query plans. <br>
Mitigation: Run the workflow against development or staging first, use least-privilege database credentials for discovery, compare before-and-after EXPLAIN results, and review production rollout separately. <br>
Risk: Deleting an existing index may regress unobserved queries if evidence is incomplete. <br>
Mitigation: Treat index deletion as a candidate until replacement coverage, non-regressing EXPLAIN output, and a rebuild path are documented. <br>


## Reference(s): <br>
- [Database index and EXPLAIN rules](references/index-rules.md) <br>
- [MySQL EXPLAIN guide](references/mysql-explain-guide.md) <br>
- [ClawHub skill page](https://clawhub.ai/jiang-zx/index-optimization) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL, MongoDB commands, shell commands, EXPLAIN summaries, and rollback statements] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes query inventory, access-pattern summary, index DDL or createIndex commands, confirmation records, EXPLAIN validation, iteration logs, final recommendations, and rollback SQL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
