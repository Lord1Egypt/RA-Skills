## Description:

Use Neon PostgreSQL conventions for Polsia apps, including migration patterns and DATABASE_URL usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agentlevier](https://clawhub.ai/user/agentlevier)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to guide agents working on Polsia apps that connect to Neon PostgreSQL, including DATABASE_URL usage, migration placement, and parameterized query conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated database migrations may modify or delete application data if applied without review.

Mitigation: Review migration code and test rollback behavior before running migrations against shared or production databases.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown guidance with JavaScript code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code is bundled with the skill.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
