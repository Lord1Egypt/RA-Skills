## Description:

Minimax Web Search uses the MiniMax Coding Plan API to search the web and understand images for an agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mirrorpromax](https://clawhub.ai/user/mirrorpromax)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to retrieve current web information and analyze JPEG, PNG, or WebP images through MiniMax-hosted search and vision tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact bundles a MiniMax API key.

Mitigation: Remove the bundled key, rotate the exposed credential, and require users to provide MINIMAX_API_KEY through their own secret-management process.

Risk: The scripts run an unpinned external MCP package through uvx.

Mitigation: Pin or vendor the MCP dependency and review it before release or installation.

Risk: The subprocess receives a broad inherited environment.

Mitigation: Pass only the environment variables required by the MiniMax MCP server.

Risk: Search terms, prompts, image paths, image URLs, and possibly image content are processed by an external service.

Mitigation: Disclose the external processing clearly and avoid sending confidential or regulated data unless approved for that service.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mirrorpromax/skills/minimax-cp-search)
- [Publisher profile](https://clawhub.ai/user/mirrorpromax)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and plain text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Search queries, prompts, image paths, and image URLs are sent to an external MiniMax service.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
