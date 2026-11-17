## Description:

Track Instagram reach, follower growth, interactions, Reels performance, and post-level engagement for an Instagram Business or Creator account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[snoopyrain](https://clawhub.ai/user/snoopyrain)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to query Instagram analytics through a Boring MCP connector and present account, Reel, post, and publishing-history metrics in clear summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP connector URL contains an embedded credential that could expose Instagram analytics, account metadata, and publishing history/status if shared.

Mitigation: Treat the connector URL like a password, avoid including it in screenshots or support logs, and revoke or regenerate it if exposure is suspected.

Risk: The skill depends on the third-party Boring service for read-only Instagram analytics access.

Mitigation: Use it only when comfortable granting Boring read access to the connected Instagram account, and review or revoke the connection when access is no longer needed.

Risk: Some post performance data comes from daily snapshots rather than real-time platform metrics.

Mitigation: Label real-time and historical snapshot metrics clearly when presenting results, especially for recent posts.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/snoopyrain/skills/instagram-analytics)
- [Boring MCP Setup Documentation](https://boring-doc.aiagent-me.com/getting-started/mcp.html)
- [Boring Documentation](https://boring-doc.aiagent-me.com)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown summaries with tables and MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Boring MCP Connector link containing an embedded read-only auth token and a connected Instagram Business or Creator account.]

## Skill Version(s):

1.0.1 (source: server release evidence; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
