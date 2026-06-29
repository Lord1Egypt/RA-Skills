## Description: <br>
PicSee URL shortener via MCP helps agents shorten URLs, generate QR-code links, inspect click analytics, and manage short links through the PicSee MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[picseeinc](https://clawhub.ai/user/picseeinc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and AI-agent operators use this skill to create short links, choose domains and tags, manage existing links, and retrieve PicSee analytics from MCP-compatible clients. Anonymous use supports one-off URL shortening, while OAuth unlocks account, management, and analytics tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Destination URLs and analytics are sent to PicSee for processing. <br>
Mitigation: Install only when PicSee is an acceptable processor for the links and analytics involved. <br>
Risk: Shortened URLs can expose secrets, tokens, or private query parameters if those values are embedded in the destination URL. <br>
Mitigation: Do not shorten URLs containing secrets or private parameters; review and remove sensitive query values before calling the short-link tool. <br>
Risk: Authenticated OAuth access can let an agent edit or delete links in the connected PicSee account. <br>
Mitigation: Require user confirmation before edit or delete actions, and clearly identify the target link before making changes. <br>
Risk: Migration cleanup commands remove legacy local PicSee token and skill files. <br>
Mitigation: Review cleanup commands with the user before running them, especially when deleting files under home-directory skill or token paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/picseeinc/skills/picsee-short-link) <br>
- [Publisher profile](https://clawhub.ai/user/picseeinc) <br>
- [GitHub repository](https://github.com/PicSeeInc/picsee-short-link) <br>
- [PicSee MCP server](https://api.picsee.io/mcp) <br>
- [PicSee developer docs](https://picsee.io/developers) <br>
- [MCP authorization specification](https://modelcontextprotocol.io/specification/draft/basic/authorization) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with MCP configuration snippets, shell commands, short-link text, and structured JSON tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [MCP over Streamable HTTP, with optional stdio bridging through mcp-remote; authenticated operations use OAuth 2.1 scopes user:read and user:write.] <br>

## Skill Version(s): <br>
3.0.2 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
