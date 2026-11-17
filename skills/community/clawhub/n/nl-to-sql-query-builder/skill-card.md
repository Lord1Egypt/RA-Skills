## Description:

Production-grade natural language to SQL toolkit for OpenClaw that supports intent classification, schema context generation, confidence scoring, clarification, fallback review, and audit logging.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhinas90](https://clawhub.ai/user/abhinas90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data application teams use this skill to help an agent convert business-language data questions into SQL workflow artifacts, including query classification, database schema context, confidence-based routing, user clarification, and audit records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database query handling can expose or modify real business data if used against production systems without additional controls.

Mitigation: Use sandbox or read-only databases until authorization, SQL safety checks, and execution review controls are added.

Risk: Audit logs and exported review records may contain sensitive user queries, generated SQL, identifiers, or business context.

Mitigation: Add log redaction, retention limits, and safe export path restrictions before using the skill with real data.

Risk: Clarification routes and debug web serving can expose query details without appropriate access controls.

Mitigation: Run clarification flows behind authenticated, non-debug routes before deployment.

Risk: One artifact file is reported to contain a syntax error and may not load unchanged.

Mitigation: Fix and test audit_logger.py before installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abhinas90/skills/nl-to-sql-query-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python code and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce SQL-related classifications, schema context JSON, confidence scores, clarification prompts, fallback review records, and audit log entries.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
