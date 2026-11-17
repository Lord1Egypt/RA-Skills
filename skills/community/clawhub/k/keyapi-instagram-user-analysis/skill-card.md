## Description:

Discover, profile, and deeply analyze Instagram users by exploring follower and following networks, posts, Reels, Stories, Highlights, tagged content, reposts, and similarity-based recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lycici](https://clawhub.ai/user/lycici)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and social media researchers use this skill to retrieve Instagram profile, content, audience, and similarity data through KeyAPI and synthesize user intelligence reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that API tokens may be stored in a local plaintext .env file.

Mitigation: Use a limited KeyAPI token, prefer setting KEYAPI_TOKEN in the shell, and delete artifact/.env if it is created.

Risk: Instagram API responses may be cached locally and remain on disk after analysis.

Mitigation: Clear .keyapi-cache when cached Instagram data should not persist.

Risk: The security summary identifies the runner as a generic KeyAPI MCP client rather than a strictly Instagram-only wrapper.

Mitigation: Review the selected platform, tool schema, and command parameters before execution and keep usage scoped to the intended Instagram workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/lycici/skills/keyapi-instagram-user-analysis)
- [KeyAPI](https://keyapi.ai/)
- [KeyAPI Instagram MCP Server](https://mcp.keyapi.ai/instagram/mcp)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON API responses from the runner]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can cache API responses locally under .keyapi-cache and can write command output to a selected file path.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
