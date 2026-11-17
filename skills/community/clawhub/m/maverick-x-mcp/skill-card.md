## Description:

Search, read, and work with X posts, users, timelines, and search through a local XMCP wrapper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to search and read X posts, users, timelines, and search results, and to create or delete posts when explicitly authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Downloaded code and dependencies may not be verified, and local-server safeguards may put account credentials or other running programs at risk.

Mitigation: Prefer a version that verifies downloaded code and dependencies, protects runtime state in a private per-user directory, authenticates the local server, and verifies process identity before termination.

Risk: Write tools can publish or delete X posts.

Mitigation: Approve each exact write action and its final content; use read-only access when it is sufficient.

## Reference(s):

- [X MCP documentation](https://docs.x.com/tools/mcp)
- [mcporter](https://github.com/openclaw/mcporter)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON]

**Output Format:** [Structured MCP responses in JSON or text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read tools return X data; post creation and deletion require explicit user confirmation.]

## Skill Version(s):

1.0.7 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
