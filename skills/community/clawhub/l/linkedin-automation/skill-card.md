## Description:

Automates LinkedIn content creation, posting, scheduling, engagement tracking, content ideation, and audience-growth workflows through a logged-in browser session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zich-dev](https://clawhub.ai/user/zich-dev)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to draft, post, schedule, and review LinkedIn activity while operating in their own logged-in LinkedIn browser session. It supports content planning, engagement workflows, analytics review, and account-growth routines.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect a real public LinkedIn account by posting, liking, commenting, requesting analytics, or scheduling future actions.

Mitigation: Review every generated post, comment, like, analytics request, and scheduled job before execution in the logged-in browser session.

Risk: Scheduled-post instructions can run later with less immediate user oversight.

Mitigation: Confirm scheduled payloads, timing, and session target before creating jobs, and periodically audit or remove scheduled tasks.

Risk: Externally supplied post content may be unsafe or unsuitable for publication.

Mitigation: Sanitize and review externally supplied content before using it in posts, comments, or scheduled jobs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zich-dev/skills/linkedin-automation)
- [LinkedIn Content Strategy Guide](references/content-strategy.md)
- [LinkedIn Engagement & Growth Tactics](references/engagement.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown-like workflow instructions with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires browser access with an active LinkedIn session; scheduled-post guidance can create actions that run later.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
