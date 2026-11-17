## Description:

Inspect local OpenClaw model usage directly from session logs. Use when asked for the current model, recent model usage, usage breakdown by model, token totals, cost summaries, per-agent usage, or daily model usage summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ranasalalali](https://clawhub.ai/user/ranasalalali)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to summarize local OpenClaw model usage, including current model activity, token and cost totals, model breakdowns, agent and session attribution, and daily usage views.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local OpenClaw session logs under ~/.openclaw/agents.

Mitigation: Install and run it only where local session-log access is acceptable, and use an explicit --root when targeting a specific log tree.

Risk: Terminal summaries and generated dashboards can reveal usage patterns, agent and session names, channels, timestamps, models, token counts, and costs.

Mitigation: Review terminal output and any generated HTML dashboard before sharing it outside the intended audience.

## Reference(s):

- [OpenClaw model usage discovery](references/discovery.md)
- [OpenClaw Model Usage on ClawHub](https://clawhub.ai/ranasalalali/skills/openclaw-model-usage)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, files]

**Output Format:** [Human-readable summaries, JSON reports, and optional self-contained HTML dashboard files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads local OpenClaw session logs from the selected agents root and can write a local dashboard file.]

## Skill Version(s):

1.2.1 (source: pyproject.toml, CHANGELOG, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
