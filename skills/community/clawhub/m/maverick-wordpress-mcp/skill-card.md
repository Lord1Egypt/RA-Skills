## Description: <br>
Read and write WordPress.com site content through WordPress.com's hosted MCP server for posts, pages, media, comments, and publishing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to manage WordPress.com posts, pages, media, comments, and site content through the official hosted MCP server with OAuth-backed access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connected OAuth grant can allow an agent to change WordPress.com content, including creating, editing, publishing, deleting, moderating, or uploading content. <br>
Mitigation: Use the least-privileged WordPress.com account available, confirm clear user intent before write or destructive actions, and read current state before making changes. <br>
Risk: Tool arguments and results transit WordPress.com's hosted MCP server. <br>
Mitigation: Do not send unrelated sensitive content through tool arguments or prompts for this connector. <br>
Risk: The OAuth grant persists until revoked, and rerunning setup with stale credentials can overwrite newer vault credentials. <br>
Mitigation: Revoke the grant in WordPress.com when access is no longer needed and rerun setup only with freshly minted OAuth credentials. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/maverick/maverick-wordpress-mcp) <br>
- [WordPress.com MCP documentation](https://developer.wordpress.com/docs/mcp/) <br>
- [WordPress.com custom MCP client authentication](https://developer.wordpress.com/docs/mcp/connect-custom-mcp-client/) <br>
- [mcporter config reference](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with shell command examples and optional JSON tool output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live tool availability and permitted actions depend on the WordPress.com MCP server catalog and the connected OAuth grant.] <br>

## Skill Version(s): <br>
1.0.5 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
