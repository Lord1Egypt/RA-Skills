## Description:

Return video/audio links or organize verified fields from user-provided public Instagram video posts and Reels. Also select this Skill for first-use Apify setup or when Apify MCP is unconnected or its authorization/readiness is unconfirmed; provide the host-specific guidance before stopping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apismith-labs](https://clawhub.ai/user/apismith-labs)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve media links returned for public Instagram video posts and Reels, or organize the post fields the service actually returns. The Skill also provides host-specific guidance for setting up Apify before first use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-provided Instagram URLs may be sent to Apify for processing, and the scanner reports that this data handling is not clearly disclosed to users.

Mitigation: Tell users that their URLs may be sent to Apify before processing, and avoid submitting URLs containing sensitive query parameters or access tokens.

## Reference(s):

- [Instagram Video Scraper API Actor on Apify](https://apify.com/apple_yang/instagram-video-scraper-api)
- [Project requirements](https://github.com/apismith-labs/instagram-ai-agent-skills/blob/main/docs/instagram-media-links-and-post-insights-prd.md)
- [Project home](https://github.com/apismith-labs/instagram-ai-agent-skills)
- [Workflow reference](references/workflow.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports Actor-returned media links and post fields while preserving source values; missing fields and uncertain input-to-result matches are identified.]

## Skill Version(s):

1.0.2 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
