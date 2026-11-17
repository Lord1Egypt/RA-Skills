## Description:

Researches Instagram profiles, posts, and Reels via the Crawlora API, returning clean JSON. Use when the user wants a public Instagram profile's stats, a specific post's media/engagement, or a user's Reels feed — instead of scraping the app.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can retrieve public Instagram profile, post, Reel, comment, and user-post data for social research, influencer vetting, and competitor audits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup targets are sent to Crawlora, and API requests consume service credits.

Mitigation: Use a dedicated Crawlora API key and review Crawlora's service information before use.

Risk: An exposed API key could allow unauthorized use of the Crawlora account.

Mitigation: Keep the key private and provide it through the CRAWLORA_API_KEY environment variable.

## Reference(s):

- [Instagram endpoint reference](reference/endpoints.md)
- [Crawlora service information](https://crawlora.net/)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Normalized JSON from public Instagram lookups]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports cursor-based pagination for Reels, comments, and user posts where available.]

## Skill Version(s):

1.0.20 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
