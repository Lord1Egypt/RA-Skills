## Description: <br>
Manages PostgreSQL-backed agent memory operations for context retrieval, prompt logging, delegation tracking, and audit recording. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Ianleme](https://clawhub.ai/user/Ianleme) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain durable PostgreSQL memory for an agent workflow, including retrieval before responses, persistence of prompt and delegation context, and per-turn audit logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can durably store chat and delegation context in PostgreSQL with broad scope. <br>
Mitigation: Limit when memory operations run, replace the hardcoded user and agent values, and scope records by user, agent, and use case before deployment. <br>
Risk: Stored memory may include secrets or regulated personal data if prompts are saved without controls. <br>
Mitigation: Do not store secrets or regulated personal data unless explicit controls are in place, and add user-facing save and forget controls. <br>
Risk: The artifact does not define retention or deletion behavior for durable memory records. <br>
Mitigation: Set retention, deletion, and audit review rules before using the skill with real operational data. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/Ianleme/memory-ops) <br>
- [Memory Ops schema.sql](references/schema.sql) <br>
- [Memory Ops queries.sql](references/queries.sql) <br>
- [Memory Ops SQL template](scripts/memory_ops_template.sql) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown guidance with PostgreSQL SQL snippets and file references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PostgreSQL with pgvector and writes memory plus audit records when applied.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
