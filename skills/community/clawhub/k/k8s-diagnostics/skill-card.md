## Description:

Kubernetes diagnostics for metrics, health checks, resource comparisons, and cluster analysis. Use when analyzing cluster health, comparing environments, or gathering diagnostic data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to review Kubernetes cluster health, inspect resource metrics, compare environments, and gather diagnostic information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Diagnostic output may contain sensitive logs or configuration, or may target an unintended cluster.

Mitigation: Use a read-only identity scoped to the intended clusters and namespaces, select the target context explicitly, and review output before sharing it.

## Reference(s):

- [Kubernetes Diagnostics on ClawHub](https://clawhub.ai/rohitg00/skills/k8s-diagnostics)
- [Publisher profile](https://clawhub.ai/user/rohitg00)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise diagnostic summaries and recommendations, optionally formatted as Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cluster health, metrics, resource comparisons, and analysis; review sensitive logs or configuration before sharing.]

## Skill Version(s):

2.0.0 (source: server-resolved release metadata, frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
