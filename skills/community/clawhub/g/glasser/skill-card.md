## Description:

Glasser helps agents search, inspect, and run paid third-party data endpoints for enrichment, web, news, image, video, maps, places, scholar, shopping, scraping, and lead lookup tasks through MCP tools or the optional CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[glasser-ai](https://clawhub.ai/user/glasser-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when a task needs external paid data that is not already available through the user's own integrations. It guides the agent to authenticate, inspect endpoint schemas and prices, run small scoped data calls, and report status, provider output, charges, and run URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid runs can spend the selected workspace balance and send task inputs to Glasser and selected providers.

Mitigation: Inspect endpoint price and charge clauses before running, start with small volume parameters, and get user approval for speculative, higher-volume, or bulk calls.

Risk: The security review notes an unpinned global CLI install path and persistent credential/tooling behavior.

Mitigation: Prefer MCP tools when possible; when the CLI is needed, use a pinned isolated install and verify authentication in the environment that will run commands.

Risk: Credential overrides can cause commands to use a different API base URL or key than the interactive login flow.

Mitigation: Avoid pasting keys into chat, check balance in the intended command environment, and review GLASSER_API_KEY and GLASSER_API_BASE_URL before paid runs.

## Reference(s):

- [Glasser documentation](https://glasser.ai/docs)
- [Glasser MCP server documentation](https://glasser.ai/docs/mcp-server.md)
- [ClawHub skill listing](https://clawhub.ai/glasser-ai/skills/glasser)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON snippets; large provider responses may be written to files and summarized.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate paid data calls after endpoint inspection; agents are instructed to report run status, provider response, charge, and Run URL.]

## Skill Version(s):

0.1.2 (source: evidence.json release and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
