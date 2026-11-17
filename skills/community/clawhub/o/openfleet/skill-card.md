## Description:

Manage your OpenFleet multi-agent workspace — create tasks, assign agents, trigger pulse cycles, manage automations, and monitor activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[serrato1](https://clawhub.ai/user/serrato1)

### License/Terms of Use:


## Use Case:

Developers and operations teams use OpenFleet to manage multi-agent workspaces from an agent environment, including creating and updating tasks, monitoring agents, triggering pulse cycles, and managing automations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can manage OpenFleet tasks, agents, automations, pulse cycles, and activity through authenticated workspace controls.

Mitigation: Use least-privilege or short-lived OpenFleet credentials and review requested task, agent, automation, and pulse changes before execution.

Risk: The skill relies on an npm-distributed MCP server invoked through npx and may require MCP client configuration changes.

Mitigation: Use a pinned and trusted @open-fleet/mcp-server version, and inspect any MCP client configuration changes before enabling the skill.

Risk: Connecting OpenFleet to an exposed OpenClaw gateway can increase remote access risk if the gateway is publicly reachable without strong controls.

Mitigation: Avoid public gateway exposure unless strong authentication, token rotation, origin restrictions, and sandboxed agent execution are in place.

## Reference(s):

- [OpenFleet](https://openfleet.sh)
- [OpenFleet API Documentation](https://app.openfleet.sh/docs)
- [OpenFleet SDK](https://www.npmjs.com/package/@open-fleet/sdk)
- [OpenFleet GitHub](https://github.com/open-fleet)
- [ClawHub OpenFleet Skill](https://clawhub.ai/serrato1/skills/openfleet)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls]

**Output Format:** [Markdown text with inline shell commands and MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OPENFLEET_API_KEY and npx to invoke @open-fleet/mcp-server.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
