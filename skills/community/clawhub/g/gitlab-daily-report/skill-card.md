## Description:

Pulls recent activity from configured GitLab repositories, summarizes commits, merge requests, issues, and pipelines, and can prepare or send Feishu daily reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chengxiansheng1](https://clawhub.ai/user/chengxiansheng1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineering leads, and project managers use this skill to gather daily GitLab activity for configured repositories and turn it into concise team progress reports, including blocker and pipeline status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Private GitLab activity and webhook configuration can be exposed through local configuration, report output, or Feishu delivery.

Mitigation: Use a narrowly scoped read-only GitLab token, keep config.json out of version control, and verify every Feishu webhook destination before sending.

Risk: The bundled HTTP client disables TLS certificate verification for GitLab and Feishu requests.

Mitigation: Avoid untrusted networks and restore TLS certificate verification before production use.

Risk: Reports can be sent to configured Feishu webhooks when the script is run without --preview, even though the skill text describes a confirmation-first workflow.

Mitigation: Run preview or raw output first, review the data, and require explicit human confirmation before invoking any non-preview send path.

## Reference(s):

- [GitLab 智能项目洞察助手 README](artifact/references/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown-like report text, Feishu post JSON, and raw JSON data when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports concise, detailed, and executive report styles; preview mode avoids webhook sending.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
