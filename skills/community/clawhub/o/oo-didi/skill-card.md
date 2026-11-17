## Description:

DiDi (mcp.didichuxing.com). Use this skill for ANY DiDi request — reading, creating, updating, and deleting data. Whenever a task involves DiDi, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using a connected DiDi account can search places, plan routes, estimate rides, manage ride orders, and inspect ongoing trip details through the oo CLI. Ride creation and cancellation require explicit user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute unverified remote software without a separate installation decision.

Mitigation: Review and install a verified CLI release separately before use; consider its automatic changes to agent skills and limit connected-account access.

Risk: Ride booking and cancellation require careful approval of the selected details.

Mitigation: Confirm pickup, destination, vehicle, price, and cancellation target carefully.

## Reference(s):

- [DiDi MCP documentation](https://mcp.didichuxing.com/api)
- [DiDi MCP homepage](https://mcp.didichuxing.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples; connector responses are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use live action schemas and may return account or trip information.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter metadata and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
