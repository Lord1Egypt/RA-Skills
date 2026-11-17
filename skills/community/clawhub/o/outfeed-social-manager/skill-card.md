## Description:

Schedule and publish social media posts to 9 platforms (Instagram, Facebook, TikTok, YouTube, X/Twitter, LinkedIn, Threads, Pinterest, Bluesky) from your AI agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mehrang0](https://clawhub.ai/user/mehrang0)

### License/Terms of Use:

MIT-0

## Use Case:

External users and social media operators use this skill to create drafts, schedule posts, publish content, manage media, and review scheduled activity across connected social accounts through Outfeed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a publishing API key with an external MCP package, so unauthorized or unintended access could affect connected social media accounts.

Mitigation: Use an Outfeed API key with permissions you are comfortable exposing to the MCP server, protect it as a secret, and review account access before installation.

Risk: The MCP package is invoked without a pinned package version, which can change behavior across installs.

Mitigation: Prefer a pinned or otherwise verified MCP package version before production use.

Risk: Publishing, deleting, or cancelling social posts can have immediate public or operational impact.

Mitigation: Keep user confirmation for destructive actions and verify scheduled times, target accounts, and timezones before execution.

## Reference(s):

- [Outfeed](https://outfeed.ai)
- [Outfeed API Key Settings](https://app.outfeed.ai/settings)
- [ClawHub Skill Page](https://clawhub.ai/mehrang0/skills/outfeed-social-manager)

## Skill Output:

**Output Type(s):** [text, markdown, API calls, configuration, guidance]

**Output Format:** [Markdown guidance with MCP tool calls and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OUTFEED_API_KEY and npx to access the Outfeed MCP server.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
