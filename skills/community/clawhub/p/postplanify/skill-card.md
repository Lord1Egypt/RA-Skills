## Description:

Schedules and manages social media posts through PostPlanify, including media uploads, analytics, and comment replies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hasancagli](https://clawhub.ai/user/hasancagli)

### License/Terms of Use:

MIT-0

## Use Case:

PostPlanify account holders and their agents use this skill to schedule and manage posts, upload media, inspect analytics, and respond to comments across connected social accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Posting or replying can publish content publicly, and deleting can permanently remove remote content.

Mitigation: Confirm the exact account, caption, media, time, reply, or item to delete before each action.

Risk: An API key grants access to sensitive account actions and data.

Mitigation: Use the least-privileged key available and keep it out of posts, replies, and logs.

Risk: Repeating failed post creation can create duplicates.

Mitigation: Inspect the error and result before attempting the action again.

## Reference(s):

- [PostPlanify skill on ClawHub](https://clawhub.ai/hasancagli/skills/postplanify)
- [PostPlanify documentation](https://postplanify.com/docs)
- [PostPlanify OpenAPI specification](https://postplanify.com/openapi.yaml)
- [API reference](references/api-reference.md)
- [Platform rules](references/platform-configs.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with shell commands and account, post, analytics, or comment summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Post and reply actions can change public content; scheduling times are expressed in the user's timezone for confirmation.]

## Skill Version(s):

1.0.0 (source: frontmatter and release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
