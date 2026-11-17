## Description:

Systematic workflow to locate and verify the Mission Control SQLite database when path assumptions fail, and reconcile frontend/backend schema mismatches.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guillaumemaka](https://clawhub.ai/user/guillaumemaka)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to debug Mission Control SQLite database location, schema, and recent task data when frontend and backend assumptions diverge.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can inspect local Mission Control database paths and recent task records during debugging.

Mitigation: Use it only in trusted local workspaces and avoid sharing database query output that may contain sensitive task data.

Risk: Schema reconciliation guidance may lead to frontend or backend changes that affect application behavior.

Mitigation: Review proposed schema, type, and backend changes before applying them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guillaumemaka/skills/mc-db-discovery)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with inline shell commands and code identifiers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local SQLite inspection commands and schema reconciliation guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
