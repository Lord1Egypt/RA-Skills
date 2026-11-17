## Description:

Provides OpenClaw performance diagnosis, configuration optimization, prompt guidance, and monitoring recommendations for reducing latency, memory use, and token consumption.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ynxiyan](https://clawhub.ai/user/ynxiyan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to diagnose performance issues, apply or adapt optimization settings, and monitor whether changes improve latency, memory use, and token consumption.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The one-click optimizer can modify local OpenClaw configuration.

Mitigation: Review the configuration diff first, make an independent backup, and test changes in a non-critical environment before applying them to a working OpenClaw setup.

Risk: Several advertised scripts appear incomplete or may fail at runtime.

Mitigation: Treat the scripts as reviewable examples until they are inspected and tested successfully in the target environment.

Risk: Monitoring values are demo-quality unless connected to real OpenClaw telemetry.

Mitigation: Use real OpenClaw metrics before relying on monitoring output for operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ynxiyan/skills/openclaw-performance-skill)
- [OpenClaw documentation](https://docs.openclaw.ai)
- [OpenClaw performance tuning](https://docs.openclaw.ai/performance)
- [OpenClaw context management](https://docs.openclaw.ai/context-management)
- [OpenClaw tool optimization](https://docs.openclaw.ai/tools)
- [Bilibili source video](https://www.bilibili.com/video/BV1CDAVziEwQ)
- [OpenClaw community discussions](https://github.com/openclaw/openclaw/discussions)
- [OpenClaw issue tracker](https://github.com/openclaw/openclaw/issues)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration and inline shell and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scripts that can write local OpenClaw configuration, generated prompts, reports, logs, and helper scripts when executed.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
