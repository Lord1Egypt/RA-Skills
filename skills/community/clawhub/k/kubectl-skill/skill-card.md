## Description:

Provides detailed kubectl command references for managing Kubernetes resources, cluster information, logs, debugging, context switching, and advanced operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xpdd](https://clawhub.ai/user/xpdd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Kubernetes operators use this skill to look up kubectl syntax, options, examples, and operational guidance for cluster administration and workload debugging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Kubectl examples can perform live cluster administration, including changes to workloads, namespaces, contexts, and resources.

Mitigation: Confirm the current kubeconfig context, namespace, target resource, and any destructive flags before allowing an agent to run generated commands.

Risk: Command examples may reveal or manipulate sensitive cluster configuration when used with options such as raw kubeconfig output or exec-style debugging.

Mitigation: Review commands for secret exposure and restrict execution to appropriately authorized environments.

## Reference(s):

- [Kubernetes kubectl reference](https://kubernetes.io/docs/reference/kubectl/)
- [Kubernetes kubectl quick reference](https://kubernetes.io/docs/reference/kubectl/quick-reference/)
- [Kubernetes kubectl command reference](https://kubernetes.io/docs/reference/kubectl/generated/kubectl/)
- [Kubernetes kubectl JSONPath support](https://kubernetes.io/docs/reference/kubectl/jsonpath/)
- [Kubectl Book](https://kubectl.docs.kubernetes.io)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and command-reference tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language kubectl reference content with command examples and operational cautions.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-04-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
