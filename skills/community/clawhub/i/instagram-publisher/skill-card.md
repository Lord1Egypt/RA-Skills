## Description: <br>
Publish posts to Instagram, including photos, carousels, Reels, and scheduled posts for Instagram Business or Creator accounts through Boring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snoopyrain](https://clawhub.ai/user/snoopyrain) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and social media operators use this skill to prepare Instagram media, publish posts, schedule posts, and manage scheduled Instagram content through a Boring MCP connector. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP connector URL contains an embedded authentication token that grants publish access to connected Instagram accounts. <br>
Mitigation: Treat the MCP URL like a password, avoid sharing it publicly, connect only accounts the agent should use, and revoke or regenerate the token if exposure is suspected. <br>
Risk: The skill can upload media and create, schedule, or cancel public Instagram posts. <br>
Mitigation: Require the agent to show the final account, media, caption, and schedule or cancellation details before taking publishing actions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/snoopyrain/instagram-publisher) <br>
- [Boring MCP Connector Documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html) <br>
- [Boring Documentation](https://boring-doc.aiagent-me.com) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Configuration] <br>
**Output Format:** [Markdown with tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce publishing or scheduling instructions that require a credential-bearing MCP connector URL.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence; artifact frontmatter says 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
