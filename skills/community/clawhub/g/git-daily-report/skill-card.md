## Description:

Generates and sends a daily report of the previous day's Git changes for configured image-tool and voc repositories, including security and general code review findings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kidok](https://clawhub.ai/user/kidok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to schedule daily DingTalk reports that summarize commits, changed files, diff statistics, and review findings for configured repositories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A persistent daily job may continue sending repository activity and review findings after installation.

Mitigation: Require an explicit preview, confirmation, and visible list/remove controls before enabling scheduled delivery.

Risk: Reports may include sensitive repository details or detected secret-like findings sent to a fixed DingTalk recipient.

Mitigation: Confirm repository ownership and DingTalk target, redact secret values, and sanitize review findings before delivery.

## Reference(s):

- [Git Daily Report on ClawHub](https://clawhub.ai/kidok/skills/git-daily-report)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown report with inline shell commands and JSON-style scheduling and message payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports target configured repositories, DingTalk delivery, and previous-day commit windows; requires git, curl, and rg.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
