## Description:

Optimize Kubernetes costs through resource right-sizing, unused resource detection, and cluster efficiency analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cluster operators use this skill to review Kubernetes costs, identify idle or overprovisioned resources, and plan capacity and cost-reduction actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Storage deletion or workload changes may cause data loss or service disruption if recommendations are inaccurate or recovery checks are skipped.

Mitigation: Start with read-only cluster permissions, explicitly select the cluster and namespaces, and require approval for deletions, resizing, or scaling. Before deleting storage, verify ownership, future consumers, retention requirements, reclaim policy, and recoverable backups; validate workload demand and rollback steps before changes.

## Reference(s):

- [Overprovisioned-resource analysis script](scripts/find-overprovisioned.py)

## Skill Output:

**Output Type(s):** [Guidance, Analysis, JSON, Shell commands]

**Output Format:** [Markdown guidance and structured JSON findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations depend on the selected cluster and namespace; validate them before applying changes.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
