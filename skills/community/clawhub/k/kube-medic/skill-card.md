## Description:

Kubernetes Cluster Triage & Diagnostics - instant AI-powered incident triage via kubectl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tkuehnl](https://clawhub.ai/user/tkuehnl)

### License/Terms of Use:

MIT

## Use Case:

Developers, SREs, and on-call engineers use this skill to triage Kubernetes cluster health, investigate failing pods and deployments, review resource pressure, and turn kubectl diagnostics into concise incident guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose Kubernetes cluster state and pod logs to the agent, including operationally sensitive or regulated data if RBAC is broad.

Mitigation: Install with read-only, namespace-scoped kubeconfig access where possible and restrict pods/log permissions for namespaces whose logs may contain sensitive data.

Risk: The optional --confirm-write path can make cluster changes such as rollbacks, restarts, scaling, pod deletion, cordon, or uncordon operations.

Mitigation: Avoid write RBAC in production unless remediation through the agent is explicitly desired, and approve write commands only after checking the exact context, namespace, target, and flags.

Risk: Cluster-wide sweeps and resource checks may touch all namespaces and can create audit noise or return excessive data in large environments.

Mitigation: Use the --namespace and --context options to scope diagnostics to the intended cluster and workload before running broad triage commands.

## Reference(s):

- [kube-medic on ClawHub](https://clawhub.ai/tkuehnl/skills/kube-medic)
- [Kubernetes kubectl installation documentation](https://kubernetes.io/docs/tasks/tools/)
- [Kubernetes Metrics Server components](https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml)
- [kind Kubernetes testing documentation](https://kind.sigs.k8s.io/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown summaries with inline shell commands and structured diagnostic findings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tool output is structured JSON that the agent parses into human-facing triage reports, tables, timelines, diagnoses, and recommended actions.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
