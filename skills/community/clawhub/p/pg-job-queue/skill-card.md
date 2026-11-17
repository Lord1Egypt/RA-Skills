## Description:

Guides agents in designing a Postgres-backed job queue with priority scheduling, batch claiming, progress tracking, retry handling, and stale job recovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to design and review a relational-database job queue that avoids separate queue infrastructure while supporting priority scheduling, worker batch claiming, retries, and progress visibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SQL and code snippets could be copied into a real database or service without adapting them to the local schema, workload, and operational constraints.

Mitigation: Review and test the generated SQL and implementation guidance in a dedicated schema or test environment before applying it to production.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with SQL and Go code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides implementation patterns and review guidance; generated SQL and code should be reviewed before use.]

## Skill Version(s):

1.0.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
