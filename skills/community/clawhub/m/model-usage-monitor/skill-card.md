## Description:

Model Usage Monitor helps OpenClaw users monitor local model usage, estimate costs, calculate cache hit rate, and receive automated cost-spike alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to inspect local model-routing logs, understand model usage and estimated cost patterns, and trigger alerts when usage crosses configured thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw logs and main-agent session metadata, which can expose sensitive usage context.

Mitigation: Install only in environments where that local metadata access is acceptable, and review the documented file paths before use.

Risk: Installation behavior can place executable code under ~/.openclaw/workspace/.lib and setup.py can add recurring OpenClaw cron execution.

Mitigation: Review or disable setup.py automatic cron behavior, and verify any OpenClaw cron entry before relying on hourly alerts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/halfmoon82/skills/model-usage-monitor)
- [Publisher profile](https://clawhub.ai/user/halfmoon82)
- [README.md](artifact/README.md)
- [clawhub.yaml](artifact/clawhub.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration]

**Output Format:** [Console, Markdown, or JSON reports with alert status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local OpenClaw logs and session metadata; alert checks can be run manually or on a recurring schedule.]

## Skill Version(s):

1.0.1 (source: server release metadata, clawhub.yaml, README.md, and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
