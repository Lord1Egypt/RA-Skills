## Description:

Kubernetes manifest security auditor that scans local YAML and JSON manifests for workload, RBAC, network, and container hardening issues mapped to CIS Kubernetes Benchmark controls and Pod Security Standards.

This skill is ready for commercial/non-commercial use.

## Publisher:

[phy041](https://clawhub.ai/user/phy041)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and security engineers use this skill to audit Kubernetes manifests before deployment or in CI. It helps identify risky pod security settings, over-permissive RBAC, missing NetworkPolicies, exposed services, and related remediation guidance without requiring cluster access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audit results may be treated as complete compliance proof even though server security evidence says the AppArmor and PSS coverage is not fully implemented.

Mitigation: Treat findings as advisory and review high-impact Kubernetes controls with a dedicated policy or compliance process before relying on deployment approval.

Risk: Copied CI examples install PyYAML without a pinned, reviewed version.

Mitigation: Pin PyYAML to an approved version in CI or internal bootstrap commands before operational use.

## Reference(s):

- [CIS Kubernetes Benchmark](https://www.cisecurity.org/benchmark/kubernetes)
- [Canlah AI homepage](https://canlah.ai)
- [ClawHub skill page](https://clawhub.ai/phy041/skills/phy-k8s-security-audit)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command snippets; scanner output may be plain text or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory security findings grouped by severity with remediation text and optional CI exit behavior.]

## Skill Version(s):

1.0.3 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
