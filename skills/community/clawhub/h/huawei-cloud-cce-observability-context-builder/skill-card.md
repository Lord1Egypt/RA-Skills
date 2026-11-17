## Description:

Collects Huawei Cloud CCE alarms, metrics, logs, and events into a structured observability context package for diagnosis handoff.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to gather Huawei Cloud CCE alarms, Kubernetes events, pod and node metrics, and logs into a timeline before handing off to diagnosis skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Read-only observability claims conflict with the security evidence that the bundled dispatcher exposes cluster-changing actions and Kubernetes secret access.

Mitigation: Review before installation, enforce a strict read-only action allowlist, and remove mutation and secret-data actions from the package.

Risk: Cloud and Kubernetes access could expose credentials, certificates, sensitive logs, or operational controls beyond the intended observability scope.

Mitigation: Use tightly scoped read-only Huawei Cloud IAM and Kubernetes RBAC, deny secrets, create/update/delete, scaling, node, EIP, and remediation permissions, use verified TLS, and store temporary certificates securely.

## Reference(s):

- [Workflow](references/workflow.md)
- [Risk Rules](references/risk-rules.md)
- [Output Schema](references/output-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [JSON context package with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes scope, signals, timeline, gaps, and next diagnostic skill recommendation.]

## Skill Version(s):

0.1.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
