## Description:

Detect N+1 query problems in application code and ORM usage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[charlie-morrison](https://clawhub.ai/user/charlie-morrison)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to find N+1 database query patterns in application code and ORM usage, then identify fixes such as eager loading, joins, batch fetching, or DataLoader patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Runtime diagnostics can expose SQL details when debug query logging is enabled.

Mitigation: Run diagnostics only in development or test environments, not against production traffic.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline code and shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces diagnostic reports, query-count guard examples, benchmark guidance, and remediation recommendations.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
