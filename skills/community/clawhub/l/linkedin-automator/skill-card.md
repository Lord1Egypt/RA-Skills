## Description:

Automate LinkedIn content creation, posting, engagement tracking, and audience growth. Use for posting content, scheduling posts, analyzing engagement metrics, generating content ideas, commenting on posts, and building LinkedIn presence. Requires browser access with LinkedIn logged in.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mpbshhx](https://clawhub.ai/user/mpbshhx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to draft, publish, schedule, and analyze LinkedIn content through a logged-in browser session, with supporting guidance for engagement and audience growth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can operate a logged-in LinkedIn account and publish posts, comments, uploads, or engagement actions from that account.

Mitigation: Review and explicitly approve every post, comment, media upload, engagement action, and scheduled job before execution.

Risk: Scheduled jobs can create future posting instructions that act later in the main session.

Mitigation: Prefer isolated, one-time workflows, audit scheduled payloads before enabling them, and remove scheduled jobs when they are no longer needed.

Risk: Untrusted topics or generated content may lead to misleading, spam-like, or policy-violating LinkedIn activity.

Mitigation: Use trusted source material, review content against LinkedIn policies, and keep activity within the documented rate limits.

## Reference(s):

- [LinkedIn Content Strategy Guide](references/content-strategy.md)
- [LinkedIn Engagement & Growth Tactics](references/engagement.md)
- [ClawHub Skill Page](https://clawhub.ai/mpbshhx/skills/linkedin-automator)
- [LinkedIn Feed](https://www.linkedin.com/feed/)
- [LinkedIn Creator Analytics](https://www.linkedin.com/analytics/creator/)
- [LinkedIn News](https://www.linkedin.com/news/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and shell workflow text with occasional JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires browser access with an active LinkedIn session; scheduled posts rely on cron-style scheduling.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
