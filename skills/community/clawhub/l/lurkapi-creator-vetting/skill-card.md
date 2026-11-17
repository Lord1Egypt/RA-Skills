## Description:

Vet an influencer or creator on TikTok, Instagram or YouTube before a deal. Pulls their profile and last ~30 posts, computes median views, engagement and posting rhythm against their own baseline, checks for bought followers, one-hit averages and heavy sponsorship, reads audience comments and scans for brand-safety risks, then gives a go or no-go scorecard. Use for influencer vetting, due diligence, comparing creators for a campaign, or "is this creator worth it".

This skill is ready for commercial/non-commercial use.

## Publisher:

[mesmerlord](https://clawhub.ai/user/mesmerlord)

### License/Terms of Use:

MIT-0

## Use Case:

Brand managers, marketers, and campaign teams can use this skill to compare prospective creators and decide whether to pursue a partnership using public profile, post, and audience-comment data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Creator lookups are sent to LurkAPI, whose privacy policy says request parameters are logged and the account's first request is retained; confidential shortlists may therefore be exposed to the service.

Mitigation: Review https://lurkapi.com/privacy before sending sensitive shortlists, keep the API key outside chat, and set a credit budget before running lookups.

## Reference(s):

- [TikTok profile API documentation](https://lurkapi.com/docs/tiktok/profile.md)
- [TikTok profile videos API documentation](https://lurkapi.com/docs/tiktok/profile-videos.md)
- [Instagram profile API documentation](https://lurkapi.com/docs/instagram/profile.md)
- [Instagram posts API documentation](https://lurkapi.com/docs/instagram/user-posts.md)
- [YouTube channel API documentation](https://lurkapi.com/docs/youtube/channel.md)
- [YouTube channel videos API documentation](https://lurkapi.com/docs/youtube/channel-videos.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown creator scorecard with a platform metrics table, verdict, strengths, risks, audience notes, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Based on public data; coverage varies by platform and does not establish audience demographics or conversions.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
