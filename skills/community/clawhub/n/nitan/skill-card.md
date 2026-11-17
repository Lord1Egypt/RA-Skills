## Description:

US Card Forum uses the local Nitan MCP stdio server to search and read uscardforum.com topics, monitor forum activity, and guide authentication for private or notification workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nitansde](https://clawhub.ai/user/nitansde)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query and summarize public US Card Forum discussions, inspect forum activity and trust-level progress, and set up authenticated notification or private-content access through Nitan MCP.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can be configured to download and run an npm package selected through environment variables.

Mitigation: Prefer a preinstalled, verified Nitan MCP package with npx --no-install; use install-on-demand only with an explicitly pinned and verified package.

Risk: Some workflows handle forum credentials or API-key setup for notifications and private content.

Mitigation: Configure credentials only through the MCP or client environment or the API-key flow, and do not paste passwords into chat.

## Reference(s):

- [Nitan MCP homepage](https://github.com/nitansde/nitan-mcp)
- [US Card Forum](https://www.uscardforum.com)
- [ClawHub skill page](https://clawhub.ai/nitansde/skills/nitan)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON-derived forum results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include forum URLs, topic IDs, authentication setup steps, and warnings when private or notification workflows need credentials.]

## Skill Version(s):

1.0.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
