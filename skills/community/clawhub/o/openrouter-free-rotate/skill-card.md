## Description:

Scans OpenRouter for zero-cost models, benchmarks and scores them by capability, and can update OpenClaw configuration with the selected models.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liligit1815](https://clawhub.ai/user/liligit1815)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to find, test, rank, and rotate free OpenRouter models for OpenClaw model routing. It can generate scan results and JSON reports, and can optionally apply the selected models to local OpenClaw configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently rewrite OpenClaw model configuration.

Mitigation: Run with --scan or --no-update first, review the selected models, and back up OpenClaw configuration files before applying changes.

Risk: API keys may be exposed if placed directly on command lines or in scheduled jobs.

Mitigation: Use OPENROUTER_API_KEY from the environment rather than putting keys in shell history, process arguments, or cron entries.

Risk: Using --restart or scheduled auto-rotation can disrupt local gateway routing.

Mitigation: Avoid --restart and unattended rotation unless persistent routing changes and gateway reloads are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liligit1815/skills/openrouter-free-rotate)
- [OpenRouter API](https://openrouter.ai/api/v1)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Terminal text, Markdown guidance, JSON reports, and OpenClaw configuration updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a JSON report, cache model test results for one hour, and update OpenClaw model configuration when run without --scan or --no-update.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
