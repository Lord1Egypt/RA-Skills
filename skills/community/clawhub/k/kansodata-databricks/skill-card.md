## Description:

Execute conservative read-only Databricks SQL through the Databricks plugin and provide safe planning output for unsupported workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kansodata](https://clawhub.ai/user/kansodata)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and data engineers use this skill to draft and execute conservative read-only Databricks SQL for single SELECT or WITH ... SELECT analysis, and to receive planning output for unsupported workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Read-only Databricks query results may still contain sensitive business data.

Mitigation: Install only where read-only Databricks SQL access is appropriate, and provide narrowly scoped warehouse, catalog, schema, and table targets.

Risk: Unsupported or mutating workflows could be requested by users.

Mitigation: Use planning output only for unsupported workflows and enforce read-only statement limits before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kansodata/skills/kansodata-databricks)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Guidance]

**Output Format:** [Markdown with Databricks SQL snippets, checklists, risk notes, and planning guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only single SELECT or WITH ... SELECT workflows; unsupported workflows receive planning output only.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
