## Description:

Search GitHub repositories, view issues, and look up user profiles via the public REST API without a token.

This skill is ready for commercial/non-commercial use.

## Publisher:

[b-gutman](https://clawhub.ai/user/b-gutman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to discover public GitHub repositories, inspect repository metadata and issue status, and retrieve public user profile information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: GitHub searches, repository names, usernames, or research interests may be sent through a third-party gateway.

Mitigation: Avoid private repository identifiers and confidential query terms; review the gateway path before using the skill with sensitive work.

Risk: The MCP configuration recommends auto-running an unpinned npm package.

Mitigation: Use a pinned mcp-remote version or a vetted local MCP client before deployment.

## Reference(s):

- [Pipeworx GitHub Pack](https://pipeworx.io/packs/github)
- [ClawHub Skill Page](https://clawhub.ai/b-gutman/skills/pipeworx-github)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return public GitHub repository, issue, and user profile data; unauthenticated GitHub API usage is rate limited.]

## Skill Version(s):

1.0.0 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
