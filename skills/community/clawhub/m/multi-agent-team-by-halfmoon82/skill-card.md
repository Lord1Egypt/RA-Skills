## Description:

Sets up configurable OpenClaw multi-agent development teams with role templates, workflows, model assignment, and operational guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[halfmoon82](https://clawhub.ai/user/halfmoon82)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to create and manage 2-10 agent OpenClaw development teams with selected roles, named teams, workflow templates, and model fallback assignments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent optimization instructions can affect OpenClaw configuration and workspace files across teams.

Mitigation: Use only in a trusted OpenClaw environment, keep backups, and enable the weekly optimizer only when cross-team configuration changes are intended.

Risk: Skill telemetry may capture prompt context or sensitive operational details.

Mitigation: Avoid sensitive prompt or secret data in telemetry and review log retention before enabling usage logging.

Risk: Unsafe team or role input handling can produce invalid configuration or workspace paths.

Mitigation: Use simple alphanumeric team and role IDs until validation is fixed, and inspect generated paths before restarting OpenClaw.

Risk: Subagent fan-out can fail because of timeouts, rate limits, spawn rejection, or unavailable channels.

Mitigation: Use timeout-governed dispatch with graded timeouts, retries, circuit breakers, and explicit failure classification.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/halfmoon82/skills/multi-agent-team-by-halfmoon82)
- [README](artifact/README.md)
- [Migration Guide v2.1 to v2.2](artifact/MIGRATION_v2.1_to_v2.2.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown guidance plus JSON/OpenClaw configuration and generated workspace files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes OpenClaw agent configuration, role workspace files, and team manifests after interactive prompts.]

## Skill Version(s):

2.2.2 (source: server release metadata and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
