## Description:

Retrieve and analyze Amplitude user events, active-user counts, retention metrics, user profiles, and activity timelines through the Pipeworx Amplitude MCP gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brucegutman](https://clawhub.ai/user/brucegutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analytics users use this skill to connect an agent to Amplitude through Pipeworx and retrieve event counts, active-user trends, retention metrics, matching user profiles, and recent user activity for date ranges and user identifiers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Amplitude analytics data and identifiable user profile or activity data may pass through an under-documented third-party MCP gateway.

Mitigation: Use the gateway only with trusted Amplitude projects, apply least-privilege credentials, and restrict or monitor profile and activity queries involving identifiable users.

Risk: Email-based user searches can expose sensitive user information when broader searches are unnecessary.

Mitigation: Avoid email-based searches unless needed for the task and prefer narrower identifiers or aggregated analytics queries.

## Reference(s):

- [Pipeworx Amplitude skill page](https://clawhub.ai/brucegutman/skills/pipeworx-amplitude)
- [Pipeworx Amplitude MCP endpoint](https://gateway.pipeworx.io/amplitude/mcp)

## Skill Output:

**Output Type(s):** [Text, API Calls, Configuration, Guidance]

**Output Format:** [Markdown and JSON configuration with agent-readable analytics results from MCP tool calls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include date ranges, granularity, event names, user identifiers, and user-property filters when invoking Amplitude tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
