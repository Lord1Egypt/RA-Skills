## Description:

Slack助手 helps agents send Slack messages, search history, manage channels, post webhook notifications, and upload files through Python Slack API examples.

This skill is ready for commercial/non-commercial use.

## Publisher:

[534422530](https://clawhub.ai/user/534422530)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and team automation agents use this skill to configure Slack notifications, channel workflows, history lookups, and file sharing for CI/CD, monitoring, collaboration, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post messages, manage channels, use webhooks, search message history, and upload local files to Slack.

Mitigation: Limit Slack app scopes to the minimum needed, require explicit confirmation before posting or uploading, and restrict file uploads to approved paths.

Risk: Slack tokens, webhook URLs, and message history may expose sensitive workspace data.

Mitigation: Store tokens and webhook URLs as secrets, avoid broad history/search access for sensitive channels, and ensure users understand privacy implications before enabling those functions.

## Reference(s):

- [Slack API App Configuration](https://api.slack.com/apps)
- [ClawHub Skill Page](https://clawhub.ai/534422530/skills/laosi-slack)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python, YAML, and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Slack credentials, selected Slack app scopes, and optional incoming webhook configuration.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
