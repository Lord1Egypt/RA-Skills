## Description:

QMD memory system telemetry for measuring index health, BM25 retrieval quality, coverage maps, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nissan](https://clawhub.ai/user/nissan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators running QMD memory backends use this skill to measure retrieval quality, index freshness, gateway events, and collection coverage. It helps diagnose degradation in local memory search before it affects agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Probe results may include sensitive query telemetry, source URIs, and local gateway-log details.

Mitigation: Run in dry-run mode first, review captured fields, and redact sensitive values before enabling persistence or local Langfuse reporting.

Risk: Live mode writes local JSON snapshots and sends probe output to a local Langfuse service over HTTP with hardcoded local keys.

Mitigation: Use live mode only when local telemetry storage and reporting are intended; prefer scoped credentials, HTTPS or safer local transport, and explicit opt-in for export.

Risk: The script reads OpenClaw gateway logs that may contain operational or personal context.

Mitigation: Limit execution to trusted local environments and review log access permissions before installing or scheduling the probe.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nissan/skills/memory-health-probe)
- [ClawHub publisher profile](https://clawhub.ai/user/nissan)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Analysis]

**Output Format:** [Console text with locally stored JSON snapshots]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can print dry-run diagnostics, trend summaries, and live local Langfuse trace results when enabled.]

## Skill Version(s):

1.0.1 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
