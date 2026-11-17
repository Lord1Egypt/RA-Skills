## Description:

Kubernetes storage management for PVCs, storage classes, and persistent volumes. Use when provisioning storage, managing volumes, or troubleshooting storage issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Kubernetes operators use this skill to inspect and manage persistent volume claims, persistent volumes, storage classes, and volume snapshots, and to troubleshoot storage issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The storage examples include PVC deletion without clearly separating or authorizing the destructive action.

Mitigation: Require explicit approval for deletion of the exact cluster, namespace, and claim; keep deletion separate from provisioning; check reclaim policy and consuming workloads; verify recoverable backups; and restrict integration permissions to intended resources.

## Reference(s):

- [Publisher profile](https://clawhub.ai/user/rohitg00)

## Skill Output:

**Output Type(s):** [Configuration, API Calls, Guidance]

**Output Format:** [Kubernetes manifests and structured cluster-tool requests with Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include changes to Kubernetes storage resources; destructive actions require explicit approval.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
