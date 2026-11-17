## Description:

Use when the user is running one or more coding agents and needs a shared control plane to coordinate work and keep an audit trail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[toddamerrill](https://clawhub.ai/user/toddamerrill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to coordinate one or more coding agents through shared objectives, session claims, progress updates, and an auditable record of agent-authored changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PlanWright records diffs, notes, test results, repository metadata, and context files as service data.

Mitigation: Avoid submitting secrets, regulated data, or proprietary details unless PlanWright retention and access controls are acceptable.

Risk: Use requires PLANWRIGHT_TOKEN configuration.

Mitigation: Provide the token only in trusted environments and avoid exposing it in recorded notes, diffs, or context files.

## Reference(s):

- [PlanWright Control Plane ClawHub skill page](https://clawhub.ai/toddamerrill/skills/planwright-control-plane)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Markdown]

**Output Format:** [Markdown guidance with tool names and workflow steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference PlanWright MCP tools and PLANWRIGHT_TOKEN configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
