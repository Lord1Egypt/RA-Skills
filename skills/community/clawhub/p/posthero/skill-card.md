## Description: <br>
This skill helps agents create drafts, schedule, publish, update, delete, and review analytics for social media posts across LinkedIn, Twitter/X, Instagram, Facebook, YouTube, TikTok, Threads, and Bluesky using the PostHero API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[a007mr](https://clawhub.ai/user/a007mr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and social media operators use this skill to manage social content from an agent conversation, including account lookup, post creation, scheduling, publishing, media upload, and analytics review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent with the PostHero API key can publish, schedule, update, or delete social content for connected accounts. <br>
Mitigation: Use a revocable API key, confirm which social accounts it can access, and require the agent to show the content, target accounts, scheduled time, and action type before any publishing, update, or deletion action. <br>
Risk: The skill requires a sensitive PostHero API key. <br>
Mitigation: Store POSTHERO_API_KEY only in the agent's approved secret or configuration store and rotate or revoke it if access changes. <br>
Risk: Deleting a post through the PostHero API removes it from PostHero but does not remove already-published content from the social media platform. <br>
Mitigation: Treat deletion as a PostHero-side action and separately verify platform removal when that is the user's intent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/a007mr/posthero) <br>
- [PostHero OpenClaw page](https://posthero.ai/openclaw) <br>
- [PostHero API base URL](https://server.posthero.ai/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON and bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires POSTHERO_API_KEY and connected social accounts; can create drafts, schedule, publish, update, delete posts, upload media, and read analytics.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
