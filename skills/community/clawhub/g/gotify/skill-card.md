## Description:

Send push notifications via Gotify when long-running tasks complete or important events occur.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jmagar](https://clawhub.ai/user/jmagar)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to send Gotify push notifications for task completion, status updates, important events, and errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Gotify server URLs and application tokens are read from local configuration or environment variables and could be exposed through weak file permissions, logs, process inspection, or plaintext HTTP.

Mitigation: Use trusted HTTPS Gotify servers, store the configuration file with owner-only permissions, avoid sending secrets in notification messages, and rotate application tokens if exposure is suspected.

## Reference(s):

- [Gotify API docs](https://gotify.net/docs/)
- [Gotify skill page](https://clawhub.ai/jmagar/skills/gotify)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute a shell script that sends a Gotify API request when configured by the user.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
