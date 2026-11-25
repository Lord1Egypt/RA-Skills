## Description:

Schedule and manage social media posts across TikTok, Instagram, Facebook, X (Twitter), YouTube, LinkedIn, Threads, Bluesky, Pinterest, Telegram, and Google Business Profile using the PostFast API. Use when the user wants to schedule social media posts, upload media for social posting, list connected social accounts, check scheduled posts (filtered by account, platform, status or date), delete posts one at a time or up to 100 per call, cross-post content to multiple platforms, manage Google Business Profile posts, geotag posts with real-world places, pick trending pre-cleared TikTok sounds, read or reply to the comments on their posts (social inbox on TikTok, Instagram, Facebook, Threads), triage or moderate comment conversations, generate a connect link so an agency client or their own app's user can connect accounts without a PostFast account, get webhooks when a post publishes or fails or an account disconnects, or automate their social media workflow. PostFast is a SaaS tool, no self-hosting required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[peturgeorgievv](https://clawhub.ai/user/peturgeorgievv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and social media operators use this skill to schedule, publish, and manage posts, comments, analytics, and account connections through PostFast across supported social platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes follower and post analytics capabilities that are not highlighted in its summary.

Mitigation: Tell the user analytics can include follower and post metrics, and retrieve them only when they fit the user's needs.

Risk: Media upload guidance does not call out that files are sent to external storage.

Mitigation: Explain the external upload step and upload only media the user has approved for that service.

## Reference(s):

- [PostFast API documentation](https://postfa.st/docs.md)
- [PostFast social media API overview](https://postfa.st/social-media-api)
- [PostFast API collection on Postman](https://www.postman.com/postfast-api/postfast/collection/a92p98v/postfast-api)
- [PostFast skill release page](https://clawhub.ai/peturgeorgievv/skills/postfast)

## Skill Output:

**Output Type(s):** [API calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON request payloads and cURL commands with explanatory Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples and step-by-step guidance for PostFast API operations.]

## Skill Version(s):

1.21.1 (source: artifact/SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
