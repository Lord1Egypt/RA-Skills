## Description:

PicSee Short Link helps agents shorten URLs, generate QR-code links, inspect click analytics, and manage PicSee links through the PicSee MCP server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[picseeinc](https://clawhub.ai/user/picseeinc)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and operators use this skill to shorten URLs, choose branded domains, attribute API usage, and retrieve analytics from PicSee inside MCP-compatible clients. Anonymous use supports one-off link creation; OAuth enables link management and analytics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OAuth authorization can allow the agent to create, edit, delete, and analyze PicSee links.

Mitigation: Grant OAuth only when the user is comfortable connecting the agent to PicSee, and confirm edit or delete operations before changing account links.

Risk: Shortened URLs, query parameters, analytics, or chart data may contain sensitive information.

Mitigation: Do not shorten URLs or render charts that contain secrets, private identifiers, signed parameters, or sensitive analytics.

Risk: The stdio bridge path can depend on an npm package fetched through npx.

Mitigation: Prefer direct Streamable HTTP MCP setup; use the bridge only when needed and pin or control the bridge dependency in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/picseeinc/skills/picsee-short-link)
- [Publisher profile](https://clawhub.ai/user/picseeinc)
- [Source repository](https://github.com/PicSeeInc/picsee-short-link)
- [PicSee MCP server](https://api.picsee.io/mcp)
- [PicSee OAuth authorization server](https://public-api-oauth.picsee.io)
- [PicSee website](https://picsee.io)
- [PicSee developer docs](https://picsee.io/developers)
- [Model Context Protocol](https://modelcontextprotocol.io)
- [MCP authorization profile](https://modelcontextprotocol.io/specification/draft/basic/authorization)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, API calls]

**Output Format:** [Markdown guidance with JSON, TOML, YAML, and shell snippets plus structured MCP tool results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [MCP responses include shortened link strings and analytics JSON; authenticated operations require OAuth user:read/user:write.]

## Skill Version(s):

3.0.2 (source: evidence release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
