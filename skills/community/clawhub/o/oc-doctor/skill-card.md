## Description:

Runs an 11-section health check for local OpenClaw installations, diagnoses configuration, session, cron, gateway, security, resource, and system-instruction issues, and presents findings with optional fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bryant24hao](https://clawhub.ai/user/bryant24hao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to audit local OpenClaw installations, understand health and security findings, and decide whether to apply guided cleanup or configuration fixes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw configuration, session, cron, log, and workspace Markdown data that may contain sensitive operational context.

Mitigation: Run it only in the intended local OpenClaw environment, review the generated report before sharing it, and confirm that secrets remain redacted.

Risk: Interactive fixes may change configuration or session files, archive workspace Markdown, or delete cache and temporary data.

Mitigation: Approve fixes only after the exact changes and deletion targets are shown; confirm critical changes individually.

Risk: The documented global npx install command is unpinned.

Mitigation: Prefer a pinned or reviewed install path before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bryant24hao/skills/oc-doctor)
- [oc-doctor homepage](https://github.com/bryant24hao/oc-doctor)
- [jq documentation](https://jqlang.github.io/jq/)
- [Windows Subsystem for Linux installation](https://learn.microsoft.com/en-us/windows/wsl/install)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown diagnostic report with severity-labeled findings, tables, inline shell commands, and interactive fix prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce structured JSON internally for system-instruction analysis; secrets are expected to be redacted in user-facing output.]

## Skill Version(s):

1.1.0 (source: ClawHub release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
