## Description:

Huawei Cloud CCE end-to-end workload pressure testing and performance evaluation using a Python SDK dispatcher.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud performance engineers use this skill to plan and run controlled Huawei Cloud CCE pressure tests, collect ELB and AOM observability evidence, evaluate elasticity phases, and generate bilingual performance reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review reports undisclosed high-risk Kubernetes and cloud actions, including cluster-wide secret export.

Mitigation: Install only in isolated test Huawei projects and CCE clusters, use least-privilege IAM and Kubernetes RBAC, and remove or block non-pressure-test actions before use.

Risk: The security guidance flags TLS certificate verification and temporary key handling as areas needing correction.

Mitigation: Enable TLS certificate verification, fix temporary key handling, and avoid production or root credentials.

Risk: Pressure tests, ELB creation, scaling, and APM injection can affect cost, capacity, and workload behavior.

Mitigation: Require explicit approval for these actions, run within a known test window, start with low traffic, and keep a rollback plan.

## Reference(s):

- [Pressure-Test Workflow](references/workflow.md)
- [Pressure-Test Risk Rules](references/risk-rules.md)
- [Pressure-Test Output Schema](references/output-schema.md)
- [ClawHub skill page](https://clawhub.ai/pintudeyudi/skills/huawei-cloud-cce-pressure-test)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, Markdown, Code]

**Output Format:** [Markdown guidance with inline shell commands, JSON evidence records, Kubernetes manifests, and Markdown, HTML, and SVG report artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated reports may include performance curves, data-gap tables, and risk-colored recommendations]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
