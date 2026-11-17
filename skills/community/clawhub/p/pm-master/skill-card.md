## Description:

PM Master helps project managers coordinate BA and SA inputs and produce project-management planning artifacts across project initiation, MVP planning, workload assessment, overall project planning, and iteration planning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo21cn](https://clawhub.ai/user/leo21cn)

### License/Terms of Use:

MIT-0

## Use Case:

Project managers and delivery teams use this skill to draft project plans, iteration plans, MVP work plans, workload assessments, and overall planning proposals from upstream requirements, architecture, constraints, and team context. Outputs are planning drafts that require review by a real project manager before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Project requirements, plans, estimates, and workflow context may be sent to a remote MCP service.

Mitigation: Use only with data appropriate for that service and obtain explicit consent before sending confidential project information.

Risk: The release ships a reusable bearer token for the remote MCP service.

Mitigation: Replace shared credentials with per-user credentials before production use.

Risk: The remote service can inject workflow rules after review.

Mitigation: Review service-provided protocol or workflow changes before relying on generated plans.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leo21cn/skills/pm-master)
- [PM MCP service endpoint](https://mcp.smartmoves.com.cn/pm/mcp)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance, Configuration]

**Output Format:** [Markdown planning documents and text responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call a remote MCP service to generate staged project-management outputs.]

## Skill Version(s):

1.8.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
