## Description:

Schedule and publish social media posts across LinkedIn, Twitter/X, Instagram, Facebook, YouTube, TikTok, Threads, and Bluesky using the PostHero API, with support for drafts, scheduled posts, immediate publishing, content management, and analytics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[a007mr](https://clawhub.ai/user/a007mr)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to manage connected PostHero social accounts from an agent, including drafting, scheduling, publishing, updating, deleting, and reviewing analytics for social posts across supported platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can publish posts immediately through connected PostHero social accounts.

Mitigation: Before publishing, require the agent to summarize the exact post text, target platforms and accounts, schedule, and whether publishing is immediate, then require clear user confirmation.

Risk: The skill can delete PostHero post records.

Mitigation: Before deletion, require the agent to identify the affected post ID and explain that deletion removes the record from PostHero but does not remove already published content from social platforms.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/a007mr/skills/posthero)
- [PostHero OpenClaw homepage](https://posthero.ai/openclaw)
- [PostHero API base URL](https://server.posthero.ai/api/v1)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, API Calls, Guidance]

**Output Format:** [Markdown guidance with bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires POSTHERO_API_KEY and connected PostHero social accounts.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
