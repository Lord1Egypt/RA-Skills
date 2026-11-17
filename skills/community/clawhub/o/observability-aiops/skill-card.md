## Description:

Operates self-hosted Prometheus, Alertmanager, Grafana, and Loki stacks with observability queries, alert and log analysis, dashboard workflows, and guarded writes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and SREs use this skill to inspect and troubleshoot self-hosted metrics, alerts, dashboards, and logs, and to perform governed changes across their observability stack.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The production setup example uses unencrypted HTTP for an endpoint that may receive credentials.

Mitigation: Use HTTPS with certificate verification before connecting credentials.

Risk: Dashboard, silence, and Prometheus configuration changes can affect live operations.

Mitigation: Start with restricted account permissions, preview changes, and require explicit approval before writes. Protect the local audit and undo databases.

## Reference(s):

- [Capabilities](references/capabilities.md)
- [Agent guardrails](references/agent-guardrails.md)
- [Setup guide](references/setup-guide.md)
- [CLI reference](references/cli-reference.md)
- [Project homepage](https://github.com/AIops-tools/Observability-AIops)
- [ClawHub release](https://clawhub.ai/zw008/skills/observability-aiops)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, API results, Shell commands, Configuration instructions]

**Output Format:** [Structured text or Markdown, with PromQL/LogQL, shell commands, and configuration examples when useful]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bounded log-query results and operational recommendations; writes can be previewed and are audited.]

## Skill Version(s):

0.13.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
