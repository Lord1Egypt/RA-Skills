## Description:

Health Check performs daily or on-demand OpenClaw environment checks for Gateway status, disk usage, memory availability, and recent log errors, then writes and sends a Markdown report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axelhu](https://clawhub.ai/user/axelhu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run scheduled or manual health checks for OpenClaw deployments and receive a concise operational report through Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu reports can expose operational health details if sent to the wrong target or populated with sensitive content.

Mitigation: Configure the Feishu group or user deliberately and limit report content to operational health signals, excluding secrets, full logs, host identifiers, and unrelated application data.

Risk: Local execution reports under data/exec-logs may retain operational details in sensitive environments.

Mitigation: Apply an appropriate retention policy for health-check execution logs before using the skill in sensitive environments.

## Reference(s):

- [Health Check detailed specification](artifact/references/spec.md)
- [ClawHub Health Check skill page](https://clawhub.ai/axelhu/skills/health-check)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration]

**Output Format:** [Markdown report with operational check results and Feishu message content]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reports under data/exec-logs/health-check/YYYY-MM-DD.md and splits Feishu messages above 3800 characters.]

## Skill Version(s):

1.0.1 (source: ClawHub release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
