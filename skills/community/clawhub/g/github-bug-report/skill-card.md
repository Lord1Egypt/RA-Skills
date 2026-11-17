## Description:

Submit bug reports to GitHub for OpenClaw issues using an issue template, GitHub API workflow, and post-submission follow-up reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[markma84](https://clawhub.ai/user/markma84)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to prepare, search for, submit, and follow up on GitHub bug reports for the OpenClaw repository.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports an embedded GitHub token.

Mitigation: Do not use this version with the embedded token; revoke the exposed token and require user-supplied credentials.

Risk: The skill can create or update GitHub issues and describes automated follow-up comments.

Mitigation: Require explicit confirmation before every GitHub write and make follow-up reminders one-time or notification-only.

Risk: Bug reports may include logs, screenshots, or configuration that contain sensitive data.

Mitigation: Sanitize logs, screenshots, and configuration before submitting them to GitHub.

## Reference(s):

- [Quick Ref - GitHub Bug Report](references/quick-ref.md)
- [ClawHub skill page](https://clawhub.ai/markma84/skills/github-bug-report)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, configuration, guidance]

**Output Format:** [Markdown with issue templates, inline shell commands, and GitHub API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or trigger GitHub issue search, create, and update operations when credentials are configured.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
