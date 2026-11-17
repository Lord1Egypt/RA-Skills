## Description:

Use when the user wants to find what's going viral in their niche, write their own version in their voice, or draft, schedule or publish posts to X (Twitter), LinkedIn, Bluesky, Mastodon, YouTube or TikTok through their Postel account, in an agent without MCP. Calls Postel's REST API with curl and a POSTEL_API_KEY.

This skill is ready for commercial/non-commercial use.

## Publisher:

[robinsadeghpour](https://clawhub.ai/user/robinsadeghpour)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to research viral post examples, draft content in their own voice, and manage posts across connected social accounts through Postel. Developers can connect an agent to a Postel workspace using its API key.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The integration uses a workspace API key, and Postel receives submitted content.

Mitigation: Store POSTEL_API_KEY securely for the intended workspace; do not paste it into chat or print it.

Risk: Scheduling or publishing sends content to connected social accounts, and publishing cannot be undone from the skill.

Mitigation: Review the exact post, destination, and time, then get clear approval before scheduling or publishing.

Risk: AI drafting endpoints consume Postel credits.

Mitigation: Use AI drafting when requested and make the credit cost clear before generating drafts.

## Reference(s):

- [Postel API documentation](https://www.postel.app/api/docs)
- [Project homepage listed in skill metadata](https://github.com/robinfaraj/postel-mcp)
- [ClawHub skill page](https://clawhub.ai/robinsadeghpour/skills/postel)

## Skill Output:

**Output Type(s):** [Text, Guidance, API Calls]

**Output Format:** [Social post text and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Post drafts, threads, and scheduling details vary by platform; YouTube and TikTok require user choices in Postel before release.]

## Skill Version(s):

1.2.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
