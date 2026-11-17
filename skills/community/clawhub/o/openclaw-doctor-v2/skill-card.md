## Description:

Checks OpenClaw system health across configuration, models, cron jobs, memory files, and installed skills, then reports findings and repair suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l6366616-lang](https://clawhub.ai/user/l6366616-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to run an explicit health check of an OpenClaw installation and receive a structured report with status, a health score, and repair suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect OpenClaw configuration, cron status, model/channel settings, and memory-related workspace files that contain private content or secrets.

Mitigation: Invoke it explicitly for diagnostics, run it only in workspaces where that inspection is acceptable, and verify that sensitive values are redacted before sharing the report.

Risk: Broad health checks can surface sensitive workspace details in the generated report.

Mitigation: Prefer metadata-only checks where possible and review the report before exposing it outside the local operating context.

## Reference(s):

- [OpenClaw documentation](https://docs.openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/l6366616-lang/skills/openclaw-doctor-v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Structured Markdown report with status indicators, command results, health score, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sensitive values such as API keys are expected to be masked before reporting.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
