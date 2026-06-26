## Description: <br>
PicSee URL shortener via MCP that helps agents shorten URLs, generate QR-code links, view click analytics, list and manage short links, and use anonymous creation or OAuth-authenticated PicSee tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[picseeinc](https://clawhub.ai/user/picseeinc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an MCP-capable agent to PicSee for creating short links, managing link metadata, and retrieving account or per-link analytics. It is useful when an agent needs link shortening, attribution, branded-domain selection, QR-code link composition, or click reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Authenticated use grants OAuth read and write access to PicSee links. <br>
Mitigation: Install only when the user trusts PicSee and is comfortable granting the documented user:read and user:write scopes. <br>
Risk: QR-code and chart recipes can share short links or analytics data with external rendering services. <br>
Mitigation: Avoid those recipes for private campaigns unless the user accepts sharing that data with the named third-party service. <br>
Risk: Migration cleanup commands remove local legacy token and CLI files. <br>
Mitigation: Review cleanup commands before execution and run only the paths that apply to the user's environment. <br>


## Reference(s): <br>
- [ClawHub Picsee Short Link listing](https://clawhub.ai/picseeinc/picsee-short-link) <br>
- [Publisher profile](https://clawhub.ai/user/picseeinc) <br>
- [PicSee MCP server](https://api.picsee.io/mcp) <br>
- [PicSee OAuth authorization server](https://public-api-oauth.picsee.io) <br>
- [PicSee repository](https://github.com/PicSeeInc/picsee-short-link) <br>
- [PicSee developer docs](https://picsee.io/developers) <br>
- [Model Context Protocol specification](https://modelcontextprotocol.io) <br>
- [MCP OAuth authorization profile](https://modelcontextprotocol.io/specification/draft/basic/authorization) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON, TOML, shell commands, URLs, and structured tool-usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill may guide agents to call remote PicSee MCP tools that return short-link URLs, account data, link metadata, and analytics.] <br>

## Skill Version(s): <br>
3.0.0 (source: server evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
