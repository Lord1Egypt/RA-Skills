## Description:

Connect to Kubernetes clusters using YAML configuration files. Use when you need to apply, validate, or manage Kubernetes resources via kubectl with YAML input. Handles kubeconfig creation, context switching, and resource deployment from YAML content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jokerzeng](https://clawhub.ai/user/jokerzeng)

### License/Terms of Use:

MIT

## Use Case:

Developers and platform engineers use this skill to validate Kubernetes YAML, apply resources with kubectl, manage kubeconfig files, switch contexts, and inspect cluster status.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can apply or validate Kubernetes resources against the active kubectl context, which may affect the wrong cluster or namespace if the context is not checked.

Mitigation: Verify the current context and namespace before running kubectl apply, and use dry-run validation before applying manifests.

Risk: The skill handles kubeconfig credentials and may create copied or long-lived credential files.

Mitigation: Use mktemp with mode 0600, avoid persistent copied kubeconfig files, and clean up temporary credential files after use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jokerzeng/skills/k8s-yaml-connect)
- [Kubernetes Official Documentation](https://kubernetes.io/docs/)
- [kubectl Cheat Sheet](https://kubernetes.io/docs/reference/kubectl/cheatsheet/)
- [Kubernetes Configuration Overview](https://kubernetes.io/docs/concepts/configuration/overview/)
- [kubeval](https://github.com/instrumenta/kubeval)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with bash commands and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs assume kubectl is installed, a Kubernetes cluster is reachable, and the user has appropriate cluster permissions.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
