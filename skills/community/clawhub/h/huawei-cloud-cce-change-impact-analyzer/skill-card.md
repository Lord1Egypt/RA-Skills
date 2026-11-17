## Description:

Huawei Cloud CCE change impact analysis skill that converts recent cluster, workload, configuration, network, security, node, and infrastructure changes into evidence-based causal attribution reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to investigate Huawei Cloud CCE incidents where recent workload releases, configuration edits, route changes, policy changes, node events, or infrastructure changes may explain an outage. It produces a timeline, evidence matrix, blast radius, risk score, conclusion, and data gaps for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The server security verdict is suspicious because the package presents this skill as read-only analysis while the bundled dispatcher exposes mutation actions that could alter or delete cloud and Kubernetes resources.

Mitigation: Install only after manual review, restrict execution to the documented read-only actions, and use tightly scoped read-only Huawei Cloud credentials and Kubernetes RBAC.

Risk: Cloud credentials and cluster access are required for analysis and could expose sensitive infrastructure data if over-scoped.

Mitigation: Use temporary or least-privilege credentials, avoid write-capable permissions, and prevent credential values from being logged or included in reports.

## Reference(s):

- [Workflow](references/workflow.md)
- [Capability Map](references/capability-map.md)
- [Output Schema](references/output-schema.md)
- [Risk Rules](references/risk-rules.md)
- [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html)
- [Huawei Cloud Python SDK Documentation](https://support.huaweicloud.com/api-cce/cce_02_0113.html)
- [ClawHub Skill Page](https://clawhub.ai/pintudeyudi/skills/huawei-cloud-cce-change-impact-analyzer)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Structured JSON with embedded Markdown report content and optional Markdown report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes trace ID, analysis window, scope, data source status, ranked changes, evidence, blast radius, confidence, and data gaps.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
