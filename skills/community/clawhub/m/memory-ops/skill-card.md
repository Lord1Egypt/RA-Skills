## Description:

Manages PostgreSQL-backed memory operations for context retrieval, prompt logging, delegation tracking, and audit event recording with Memory_openclaw and pgvector.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianleme](https://clawhub.ai/user/ianleme)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to set up and follow a PostgreSQL-backed memory workflow for retrieving context, saving prompt and delegation records, and auditing read/write cycles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shared long-term memory may retain raw prompts, delegation payloads, or sensitive context beyond user expectations.

Mitigation: Use only in a private, single-user environment unless consent, redaction, retention, deletion, and access controls are added.

Risk: The SQL defaults use a hardcoded user identity and global scope.

Mitigation: Replace them with authenticated tenant, user, and session parameters before installation.

Risk: The bootstrap script seeds persistent behavioral rules that may not match the user's intended operating policy.

Mitigation: Remove or explicitly approve seeded rules before running the bootstrap script.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ianleme/skills/memory-ops)
- [schema.sql](references/schema.sql)
- [queries.sql](references/queries.sql)
- [memory_ops_template.sql](scripts/memory_ops_template.sql)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with SQL code and PostgreSQL shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires review before execution because the SQL defaults use a fixed user identity, global scope, prompt retention, and seed memory entries.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
