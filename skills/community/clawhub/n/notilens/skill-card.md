## Description:

Send real-time alerts to NotiLens from any script, app, or AI agent - task lifecycle events, errors, completions, metric tracking, and custom alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notilens](https://clawhub.ai/user/notilens)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send structured task status, error, completion, metric, and human-input alerts from scripts, applications, or agents to NotiLens.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Notification payloads are sent to NotiLens and may expose sensitive task details if populated with secrets, personal data, internal hostnames, raw stack traces, long-lived download links, or privileged approval URLs.

Mitigation: Only send task alert data that is intended for NotiLens, keep messages concise, and exclude sensitive values from payload fields including message, meta, open_url, and download_url.

## Reference(s):

- [NotiLens homepage](https://www.notilens.com)
- [ClawHub skill page](https://clawhub.ai/notilens/skills/notilens)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with JSON payload examples and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NOTILENS_TOKEN, NOTILENS_SECRET, and curl to send webhook notifications.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
