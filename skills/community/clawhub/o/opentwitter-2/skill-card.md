## Description:

Twitter/X and meme evidence data via the 6551 API. Supports user profiles, tweet search, user tweets, follower events, deleted tweets, KOL followers, meme token evidence, and meme activity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infra403](https://clawhub.ai/user/infra403)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve Twitter/X profiles, posts, activity, and meme-token evidence through the 6551 API. It can also add or remove accounts in a persistent monitoring list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API token is sent as a bearer credential, and the WebSocket example places it in the connection URL, where URLs may be captured in logs.

Mitigation: Keep OPENNEWS_TOKEN private, avoid logging or sharing authenticated URLs, and rotate the token if it is exposed.

Risk: Adding or deleting a Twitter watch entry changes a persistent monitoring list.

Mitigation: Review the target account and monitoring options, and get clear authorization before making watch-list changes.

## Reference(s):

- [6551 API service](https://ai.6551.io)
- [Get a 6551 API token](http://app.newsliquid.com/mcp)

## Skill Output:

**Output Type(s):** [JSON, Text, Guidance]

**Output Format:** [Structured API data with concise text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an OPENNEWS_TOKEN; API rate limits apply, with most listed retrieval requests capped at 100 results.]

## Skill Version(s):

0.1.2 (source: ClawHub release metadata; skill frontmatter declares 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
