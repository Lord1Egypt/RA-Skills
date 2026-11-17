## Description:

Publish or schedule posts to Instagram, TikTok, YouTube, X, LinkedIn, Threads, Bluesky, Pinterest and Facebook through Mellow Hub using its remote MCP server or REST API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[melodywco-byte](https://clawhub.ai/user/melodywco-byte)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, agents, and social publishing operators use this skill to connect to Mellow Hub, validate posts against network rules, and prepare, schedule, or publish cross-network social posts with appropriate review and credential controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could publish public social posts or schedule content through connected accounts.

Mitigation: Use review mode or narrow OAuth/API-key scopes unless autopilot publishing is explicitly intended, and validate every post before creation.

Risk: API keys, OAuth tokens, or signed upload URLs could expose account access if copied into chat or logs.

Mitigation: Keep credentials in environment variables, refer to keys symbolically, and avoid echoing or storing secrets.

Risk: Draft content and media details are sent to Mellow Hub for validation and publishing workflows.

Mitigation: Install and use the skill only when the user intends to share that content with Mellow Hub and connected social platforms.

## Reference(s):

- [Mellow Hub Docs](https://www.mellow.world/hub/docs)
- [Mellow Hub MCP Endpoint](https://www.mellow.world/mcp)
- [Mellow Hub REST API](https://www.mellow.world/api/hub/v1)
- [Schedule Posts API Guide](https://www.mellow.world/hub/guides/schedule-posts-api)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with JSON configuration and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP setup, REST examples, validation steps, idempotency guidance, and per-network posting constraints.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
