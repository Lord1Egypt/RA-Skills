## Description:

Use when performing periodic, low-risk health checks on Huawei Cloud CCE clusters: daily inspection, quick health check, heartbeat summary, or continuous operations report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations teams use this skill to run quick-first Huawei Cloud CCE health inspections, summarize cluster status, classify P0/P1/P2 risks, and prepare read-only handoff recommendations when anomalies need follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents itself as read-only cluster inspection, but the packaged dispatcher exposes powerful cloud and Kubernetes administration actions.

Mitigation: Review before installing as an admin-capable Huawei Cloud tool; use tightly scoped read-only IAM/RBAC, avoid passing AK/SK on command lines, avoid Secret and kubeconfig actions, and prefer a package that separates inspection from remediation or enforces a read-only action allowlist.

## Reference(s):

- [Workflow](references/workflow.md)
- [Risk Rules](references/risk-rules.md)
- [Output Schema](references/output-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON inspection reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cluster health summaries, check results, classified risks, recommended follow-ups, and optional report file paths.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
