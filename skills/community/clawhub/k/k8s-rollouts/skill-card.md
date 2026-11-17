## Description:

Progressive delivery with Argo Rollouts and Flagger. Use when implementing canary deployments, blue-green deployments, or traffic shifting strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to inspect and manage canary and blue-green deployments with Argo Rollouts or Flagger, including monitoring rollout health, shifting traffic, promoting, and aborting changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rollout operations can change running applications.

Mitigation: Restrict access to the intended cluster and namespaces, and use the skill only for explicit rollout requests.

Risk: Promoting a rollout before health checks complete can advance an unhealthy change.

Mitigation: Check rollout status and analysis results before promotion, and establish whether automatic aborts are allowed.

Risk: Full promotion skips analysis, pauses, and remaining rollout steps.

Mitigation: Use full promotion only when deliberately choosing to bypass those safeguards.

## Reference(s):

- [Argo Rollouts: promote](https://argoproj.github.io/argo-rollouts/generated/kubectl-argo-rollouts/kubectl-argo-rollouts_promote/)

## Skill Output:

**Output Type(s):** [Guidance, Configuration, Code]

**Output Format:** [Markdown with tool-call examples and YAML manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Kubernetes Rollout or Flagger Canary manifest examples.]

## Skill Version(s):

2.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
