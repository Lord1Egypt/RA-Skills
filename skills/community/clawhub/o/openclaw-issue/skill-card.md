## Description:

Create and submit GitHub Issues for OpenClaw and ClawHub projects with templates for skill appeals, bug reports, feature requests, and questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[luduoxin](https://clawhub.ai/user/luduoxin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw or ClawHub users use this skill to draft GitHub issues for skill appeals, bugs, feature requests, and questions. It guides the agent to collect issue details and produce a prefilled issue URL or optional GitHub CLI command for submission.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Issue text inserted directly into shell snippets can cause unsafe local command execution.

Mitigation: Generate prefilled issue URLs with structured URL encoding or safe argument passing, and avoid the GitHub CLI path unless commands are built without shell interpolation.

Risk: Automatically submitted issues may contain incorrect, incomplete, or misleading details.

Mitigation: Prefer the prefilled URL flow and have the user review the title, body, labels, and target repository before submitting the issue.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/luduoxin/skills/openclaw-issue)
- [Publisher profile](https://clawhub.ai/user/luduoxin)
- [OpenClaw ClawHub issues](https://github.com/openclaw/clawhub/issues)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown guidance with issue templates, generated URLs, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided issue details and a GitHub account for final issue submission.]

## Skill Version(s):

1.0.0 (source: server release evidence and clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
