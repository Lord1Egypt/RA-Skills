## Description:

Manage social media through PostNext - schedule, publish, and analyze posts across Twitter/X, Instagram, LinkedIn, Threads, YouTube, TikTok, and Bluesky via the PostNext public API. Use when the user wants to compose, schedule, or publish social posts, upload media for posts, check what is queued, cancel a scheduled post or delete a post from PostNext, read social analytics (engagement, best time to post, audience growth) or refresh them with an analytics sync, and has a PostNext account and API key. Publishing, scheduling, cancelling, deleting, uploading and analytics sync always preview first and need the user's approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[postnextio](https://clawhub.ai/user/postnextio)

### License/Terms of Use:

MIT-0

## Use Case:

Social media managers, creators, and account owners can use the skill to compose, publish or schedule posts, manage queued posts and media, and review analytics for their connected social channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repeating a confirmed publish or schedule can create duplicate posts, and confirmation codes can be reused.

Mitigation: Review each exact preview, avoid replaying a confirmed command, and check the queue before scheduling again.

Risk: Uploaded media leaves the user's device and is handled by PostNext and its storage provider.

Mitigation: Upload only the media the user asked to attach and review the upload preview before confirming.

Risk: If no channel is specified, the helper may choose the first matching connected account.

Mitigation: Select the intended channel explicitly in the command.

## Reference(s):

- [PostNext Social Manager on ClawHub](https://clawhub.ai/postnextio/skills/postnext-social-manager)
- [Posts reference](references/posts.md)
- [Media reference](references/media.md)
- [Channels reference](references/channels.md)
- [Analytics reference](references/analytics.md)
- [Errors reference](references/errors.md)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON, Guidance]

**Output Format:** [Shell commands and text instructions, with JSON API data and summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Account-changing operations display a preview and require an explicit confirmation code before execution.]

## Skill Version(s):

0.1.6 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
