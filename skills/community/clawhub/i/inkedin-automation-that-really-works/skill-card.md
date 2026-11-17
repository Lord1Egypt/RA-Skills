## Description:

LinkedIn automation - post with image upload, comment with mentions, edit or delete comments, repost, read feed, analytics, like monitoring, engagement tracking, and content calendar with approval workflow through Playwright with a persistent browser profile.

This skill is for research and development only.

## Publisher:

[red777777](https://clawhub.ai/user/red777777)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to automate personal LinkedIn publishing, engagement review, profile analytics, style learning, and approval-based scheduled posting. It is suited to supervised personal productivity workflows where public account actions are reviewed before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post, comment, repost, edit comments, and delete comments on a real public LinkedIn account.

Mitigation: Require explicit user confirmation for every public or destructive action, showing the exact text, URL, image path, and action before execution.

Risk: Persistent browser, like-monitor, style-profile, and content-calendar state can retain account session or personal content context.

Mitigation: Use a dedicated LinkedIn browser profile and restrict local state file permissions to the intended user.

Risk: The content-calendar webhook updates posting state and can be installed as a long-running service.

Mitigation: Keep the webhook bound to localhost unless authentication, authorization, and least-privilege service configuration are added.

Risk: Browser automation is configured with a no-sandbox Chromium argument.

Mitigation: Remove the no-sandbox argument before trusted deployment unless the runtime environment strictly requires it and has compensating isolation.

Risk: Commands accept LinkedIn post or profile URLs and automate navigation.

Mitigation: Validate URLs so automation only visits expected LinkedIn domains and paths.

## Reference(s):

- [Content Calendar Integration](references/content-calendar.md)
- [LinkedIn Content Strategy](references/content-strategy.md)
- [LinkedIn DOM Patterns Reference](references/dom-patterns.md)
- [LinkedIn Engagement Guide](references/engagement.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return JSON and may create local browser, style-profile, webhook action, and content-calendar state files.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
