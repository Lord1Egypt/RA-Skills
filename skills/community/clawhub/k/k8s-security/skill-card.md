## Description:

Audit Kubernetes RBAC, enforce policies, and manage secrets. Use for security reviews, permission audits, policy enforcement with Kyverno/Gatekeeper, and secret management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Kubernetes RBAC, policies, secrets access, and network isolation. It provides audit checklists, policy examples, and remediation guidance for security reviews.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The RBAC audit can miss dangerous administrator access and may present incomplete results as comprehensive.

Mitigation: Correct the binding queries and remove the blanket exclusion of system-prefixed subjects before relying on audit results.

Risk: Audits and suggested changes can affect sensitive cluster permissions or secrets.

Mitigation: Select the intended cluster and namespaces, use read-only access for audits, and authorize secret access or configuration changes separately.

## Reference(s):

- [RBAC Patterns](RBAC-PATTERNS.md)
- [Kyverno MCP Server](https://github.com/nirmata/kyverno-mcp)

## Skill Output:

**Output Type(s):** [Analysis, Code, Configuration, Guidance]

**Output Format:** [Markdown with tool-call examples and YAML manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cluster-specific audit guidance and policy examples; validate recommendations against the target cluster.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
