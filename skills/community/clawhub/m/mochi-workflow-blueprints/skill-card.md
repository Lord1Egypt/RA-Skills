## Description:

Validate a workflow dependency graph, detect cycles and separate read-only steps from external mutations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and workflow designers use the skill to check dependencies, detect cycles, and identify steps that may change external systems before deciding how to carry out a workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A validated workflow plan may be mistaken for an automation that has already run.

Mitigation: Describe the result as a plan; confirm authorization and verify the outcome separately before reporting any live action as completed.

Risk: Repeated execution of mutating workflow steps can cause duplicate external changes.

Mitigation: Set retry limits and define idempotency before carrying out repeated writes.

## Reference(s):

- [Input contract](references/input.md)
- [中文用法](references/zh-CN.md)
- [MochiLab homepage](https://mochilab.bz)
- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-workflow-blueprints)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Files]

**Output Format:** [JSON report with an execution order and a list of mutating steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline plan validation; does not schedule workflows or execute external actions.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
