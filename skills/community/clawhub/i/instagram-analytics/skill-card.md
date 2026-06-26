## Description: <br>
Track Instagram performance metrics such as reach, followers, engagement, Reels performance, and post-level analytics for connected Instagram Business or Creator accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External social media operators, creators, and analysts use this skill to inspect read-only Instagram Business or Creator account analytics through the Boring MCP connector and present account, Reels, post, and trend summaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP Connector URL contains an embedded authentication token. <br>
Mitigation: Treat the connector URL like a password, add it only to trusted connector settings, and revoke or regenerate it if it may have been exposed. <br>
Risk: The skill depends on the third-party Boring service for read-only Instagram analytics access. <br>
Mitigation: Install only when the user trusts Boring with access to Instagram Business or Creator analytics and account metadata. <br>
Risk: The connector is limited to analytics and account metadata, so it will not modify or publish Instagram content. <br>
Mitigation: Use it for reporting and analysis workflows, and reconnect or regenerate credentials through Boring if access errors indicate token expiry or invalid credentials. <br>


## Reference(s): <br>
- [ClawHub Instagram Analytics skill page](https://clawhub.ai/snoopyrain/instagram-analytics) <br>
- [Boring MCP connector setup documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [Boring API documentation](https://boring-doc.aiagent-me.com) <br>
- [Boring settings](https://boring.aiagent-me.com/settings) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown summaries and tables describing Instagram account, Reels, post, and historical performance metrics.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a Boring MCP Connector URL with an embedded authentication token and a connected Instagram Business or Creator account.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
