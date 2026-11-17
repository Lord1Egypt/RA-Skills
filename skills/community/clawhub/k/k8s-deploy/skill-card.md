## Description:

Deploy and manage Kubernetes workloads with progressive delivery. Use for deployments, rollouts, blue-green, canary releases, scaling, and release management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rohitg00](https://clawhub.ai/user/rohitg00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to deploy, inspect, scale, and roll back Kubernetes workloads, including canary and blue-green releases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup may install powerful, persistent cluster components without fully explaining their scope.

Mitigation: Review controller installation separately from application deployment; confirm the target cluster, pin and inspect installation manifests, review cluster-wide permissions and monitoring scope, and agree on removal steps.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/rohitg00/skills/k8s-deploy)
- [Publisher profile](https://clawhub.ai/user/rohitg00)
- [Rollout workflows](artifact/ROLLOUTS.md)
- [Deployment strategy guide](artifact/references/STRATEGIES.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with tool-call examples, shell commands, and YAML manifests]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples depend on the target cluster, namespace, workload, and rollout settings.]

## Skill Version(s):

2.0.0 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
