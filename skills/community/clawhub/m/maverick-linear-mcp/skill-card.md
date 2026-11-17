## Description:

Read and write Linear workspace data via Linear's hosted MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to search and read Linear workspace data, and to create or update issues, projects, and cycles through Linear's hosted MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The connected Linear account may create or change workspace records, including in batches.

Mitigation: Confirm the intended records and scope before write operations; review batch changes carefully.

Risk: Rerunning setup with stale OAuth credentials can overwrite newer rotated credentials and interrupt access.

Mitigation: Rerun setup only with freshly provisioned OAuth credentials, and re-authorize if the grant has been revoked.

## Reference(s):

- [Linear MCP documentation](https://linear.app/docs/mcp)
- [mcporter configuration documentation](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md)

## Skill Output:

**Output Type(s):** [API Calls, Structured data, Text]

**Output Format:** [Structured MCP results and natural-language responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Available tools and arguments follow the live Linear MCP catalog.]

## Skill Version(s):

1.0.3 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
