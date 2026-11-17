## Description:

Operate Kubernetes clusters through read-only diagnostics and common workload, rollout, storage, namespace, and node operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to inspect cluster health, diagnose workload issues, and carry out scoped Kubernetes operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cluster writes can delete workloads or disrupt nodes when permitted by the connected Kubernetes account.

Mitigation: Start with a dedicated read-only account restricted to the intended cluster and namespaces; grant write access only when needed.

Risk: The MCP interface does not require an approval check before destructive actions, and deletions may be irreversible.

Mitigation: Require approval for destructive calls in the agent client, preview changes, and pin a reviewed package version.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zw008/skills/k8s-aiops)
- [Project homepage](https://github.com/AIops-tools/K8s-AIops)
- [Capabilities](artifact/references/capabilities.md)
- [CLI reference](artifact/references/cli-reference.md)
- [Setup and security guide](artifact/references/setup-guide.md)
- [Agent guardrails](artifact/references/agent-guardrails.md)

## Skill Output:

**Output Type(s):** [Text, Analysis, Guidance]

**Output Format:** [Text summaries with structured Kubernetes resource details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results reflect the selected cluster and namespace; write operations depend on kubeconfig permissions.]

## Skill Version(s):

0.16.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
