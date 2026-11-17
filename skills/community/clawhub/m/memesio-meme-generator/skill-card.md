## Description:

Use for meme generation with Memesio through MCP: search meme templates, add captions to templates or uploaded images, create meme agent accounts, and generate AI memes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyalerio](https://clawhub.ai/user/heyalerio)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect agents or MCP clients to Memesio, search meme templates, caption templates or uploaded images, create agent accounts, and generate AI memes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, captions, uploaded images, image URLs, and generated meme requests may be sent to Memesio's hosted service.

Mitigation: Avoid sending confidential images, secrets, regulated data, or internal-only URLs, and use private visibility when appropriate.

Risk: Created Memesio API keys can grant access to keyed tools.

Mitigation: Treat API keys as secrets and pass them only to keyed tool calls that require them.

## Reference(s):

- [Memesio MCP developer documentation](https://memesio.com/developers/mcp)
- [Memesio MCP endpoint](https://memesio.com/api/mcp)
- [tools.txt](references/tools.txt)
- [ClawHub skill page](https://clawhub.ai/heyalerio/skills/memesio-meme-generator)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, API Calls]

**Output Format:** [Markdown with JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include MCP tool names, connection settings, and example request payloads.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
