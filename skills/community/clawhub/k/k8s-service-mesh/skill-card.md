## Description:

Manage Istio service mesh for traffic management, security, and observability. Use for traffic shifting, canary releases, mTLS, and service mesh troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Kubernetes operators use this skill to inspect and manage Istio service meshes, including traffic routing and canary releases, mTLS policies, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Production traffic mirroring may expose request data to an unauthorized destination or duplicate writes and other side effects.

Mitigation: Start in staging with namespace-limited permissions; confirm the target cluster and intended changes, save the current configuration for rollback, and verify the mirror destination is authorized and safe for duplicate requests.

## Reference(s):

- [Kubernetes Service Mesh (Istio) on ClawHub](https://clawhub.ai/rohitg00/skills/k8s-service-mesh)

## Skill Output:

**Output Type(s):** [Configuration, Shell commands, Guidance]

**Output Format:** [Markdown with YAML configuration and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes review and verification steps for Istio changes.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
