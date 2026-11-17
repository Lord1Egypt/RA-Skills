## Description:

Huawei Cloud CCE service topology dependency impact analysis skill that traces Service/Ingress/Pod/Node propagation paths and upstream/downstream blast radius.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud operations engineers use this skill to analyze Huawei Cloud CCE incidents, map Kubernetes Service/Ingress/Pod/Node propagation paths, estimate blast radius, and produce evidence-backed impact reports with confidence limits.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill presents itself as read-only impact analysis, but its bundled dispatcher exposes destructive CCE and Kubernetes operations plus risky credential handling.

Mitigation: Review this skill before installing. Use only narrowly scoped read-only Huawei Cloud IAM and Kubernetes RBAC credentials, and do not expose production write-capable credentials to its dispatcher unless the package is changed to remove or block all mutation and secret-export actions.

## Reference(s):

- [Workflow pipeline and scoring rules](references/workflow.md)
- [Read-only boundaries and handoff rules](references/risk-rules.md)
- [Output structure specification](references/output-schema.md)
- [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html)
- [Huawei Cloud Python SDK Documentation](https://support.huaweicloud.com/api-cce/cce_02_0113.html)
- [ClawHub skill page](https://clawhub.ai/pintudeyudi/skills/huawei-cloud-cce-dependency-impact-analyzer)

## Skill Output:

**Output Type(s):** [analysis, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON results with Markdown impact reports, evidence tables, propagation paths, Mermaid topology, and confidence limits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include report_markdown and an optional report_file path from the dependency impact analysis action]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
