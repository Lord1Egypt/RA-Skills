## Description: <br>
Design, analyze, optimize and evolve database schemas for schema design, SQL versus NoSQL selection, normalization review, index planning, migration generation, and EXPLAIN plan interpretation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[felix-antonio-sl](https://clawhub.ai/user/felix-antonio-sl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design or review database schemas, choose an appropriate database engine, plan indexes, generate migrations with rollback, and interpret query plans. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated schema, index, or migration guidance can be incorrect for a live workload or engine-specific behavior. <br>
Mitigation: Review proposed DDL, indexes, and migration scripts against the target database and test them before production use. <br>
Risk: Destructive migration steps can cause data loss if applied without preparation. <br>
Mitigation: Take a logical backup before destructive changes and require a rollback path for every migration. <br>


## Reference(s): <br>
- [database-designer reference](references/database-design-reference.md) <br>
- [Database Selection Decision Tree](references/database_selection_decision_tree.md) <br>
- [Index Strategy Patterns](references/index_strategy_patterns.md) <br>
- [Database Normalization Guide](references/normalization_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with SQL, Mermaid ERD, Prisma, JSON Schema, or shell command blocks as requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Emits one primary artifact per response and notes trade-offs, information loss, indexing recommendations, and migration next steps when applicable.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
