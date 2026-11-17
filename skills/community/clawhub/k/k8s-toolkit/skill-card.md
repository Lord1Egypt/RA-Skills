## Description:

K8s容器编排工具 helps developers review Kubernetes YAML and cluster exports for common resource, probe, selector, image, network policy, and RBAC issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to inspect Kubernetes manifests or read-oriented kubectl exports before deployment or during troubleshooting. It returns prioritized findings, remediation guidance, and configuration examples for reliability and security issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect Kubernetes manifests and run read-oriented kubectl commands against a configured cluster.

Mitigation: Review commands before execution and prefer limited namespace or file-based inputs instead of broad production cluster scope.

Risk: Exported Kubernetes YAML may contain sensitive cluster configuration or Secrets.

Mitigation: Redact secrets and sensitive metadata before sharing inputs with the agent or storing outputs.

Risk: The security review flags broad trigger language and only partial safety boundaries.

Mitigation: Use the skill for explicit Kubernetes review tasks and keep human review in the loop for cluster access and remediation changes.

## Reference(s):

- [Kubernetes kubectl installation documentation](https://kubernetes.io/docs/tasks/tools/)
- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/k8s-toolkit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML, JSON, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include risk summaries, compliance scores, findings, remediation suggestions, and kubectl command examples.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
