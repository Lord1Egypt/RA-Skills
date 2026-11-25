## Description:

Helps an agent create social media drafts from templates, review them with the user, schedule or cross-post approved content, and read post analytics through Orshot MCP or REST.

This skill is ready for commercial/non-commercial use.

## Publisher:

[orshot](https://clawhub.ai/user/orshot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media teams can use the skill to prepare, review, schedule, and track social posts across connected accounts. It supports template-rendered media and posts prepared from existing public media URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends post content and media through Orshot's hosted MCP service or REST API; the supplied scan did not fully resolve how external requests handle data.

Mitigation: Review Orshot's data handling information and decide what account, post, and media data to send before connecting accounts or publishing.

## Reference(s):

- [Orshot publishing overview](https://orshot.com/docs/publish/introduction.md)
- [Orshot MCP server setup](https://orshot.com/docs/integrations/mcp-server.md)
- [Social posting guidelines and platform limits](https://orshot.com/docs/publish/social-posting-guidelines.md)
- [Social account connection guide](https://orshot.com/docs/publish/connect-account.md)
- [Orshot publishing pricing](https://orshot.com/docs/publish/pricing.md)
- [Publish from the Orshot API](https://orshot.com/docs/publish/publish-from-api.md)
- [Post approval flows](https://orshot.com/docs/approval-flows/introduction.md)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown, API Calls]

**Output Format:** [Natural language guidance, social post drafts, and structured MCP or REST API arguments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include captions, draft and schedule details, and analytics summaries. Posts are held for user review unless the user explicitly asks to publish.]

## Skill Version(s):

1.3.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
