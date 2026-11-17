## Description:

Crowdin (crowdin.com). Use this skill for ANY Crowdin request — reading, creating, and updating data. Whenever a task involves Crowdin, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and localization teams use this skill to inspect Crowdin projects, branches, directories, and files, and to create branches, directories, or upload source files through their connected Crowdin account. It checks the live action schema before preparing requests and requires confirmation for actions marked as writes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may execute downloaded CLI software without clear approval for broader local changes.

Mitigation: Review and approve CLI installation separately; prefer a verified, fixed release over executing downloaded scripts.

Risk: The connected Crowdin account may expose more data or write permissions than needed.

Mitigation: Connect only the account and permissions required for the task, and keep the documented confirmation steps for write actions.

## Reference(s):

- [Crowdin](https://crowdin.com)
- [Crowdin API v2 documentation](https://developer.crowdin.com/api/v2/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Text, Guidance]

**Output Format:** [Crowdin connector results and JSON action payloads, with shell command examples and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs depend on the live Crowdin schema; write actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
