## Description:

Scans Huawei Cloud CCE clusters for availability risks such as single replicas, missing PodDisruptionBudgets, health probe gaps, AZ imbalance, gateway concentration, and resource overcommit.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud platform, Kubernetes, and SRE teams use this skill to assess Huawei Cloud CCE cluster availability posture, identify high-availability gaps, and produce risk-rated remediation guidance before operational changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Server security evidence says the package is advertised as a read-only availability scanner but exposes reachable actions that can change or disclose sensitive Huawei CCE infrastructure.

Mitigation: Before installing, require a narrowed dispatcher or package that exposes only the documented read-only scan actions.

Risk: The skill uses Huawei IAM credentials and Kubernetes access to inspect cluster resources.

Mitigation: Run only with tightly scoped read-only Huawei IAM and Kubernetes RBAC that denies writes, Secret data access, and kubeconfig or certificate generation unless explicitly needed and separately approved.

Risk: Generated remediation plans or YAML suggestions can be wrong when cluster data is incomplete or workload constraints are not understood.

Mitigation: Review findings, data gaps, impact scope, rollback method, and verification metrics before applying any remediation outside the scanner.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pintudeyudi/skills/huawei-cloud-cce-availability-risk-scanner)
- [Workflow](references/workflow.md)
- [Risk Rules](references/risk-rules.md)
- [Output Schema](references/output-schema.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON reports with risk issues, summaries, data gaps, recommendations, remediation plans, and optional output files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Huawei Cloud credentials, target region, and CCE cluster context; optional output_dir can write availability-risk summary and report files.]

## Skill Version(s):

0.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
