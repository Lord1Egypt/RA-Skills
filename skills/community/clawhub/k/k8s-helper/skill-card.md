## Description:

Operate Kubernetes clusters via kubectl with a user-supplied local or remote kubeconfig.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoshino-s](https://clawhub.ai/user/yoshino-s)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to inspect, manage, and debug Kubernetes resources through kubectl against clusters identified by local or remote kubeconfig files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform powerful Kubernetes cluster administration through supplied kubeconfigs.

Mitigation: Use only least-privilege kubeconfigs from trusted sources and review intended kubectl operations before execution.

Risk: Remote kubeconfigs may contain sensitive credentials and can be cached persistently.

Mitigation: Prefer local kubeconfig files, avoid remote kubeconfig URLs when possible, and clear the cache after use if remote kubeconfigs are used.

Risk: The wrapper may download a kubectl executable if kubectl is not already available.

Mitigation: Prefer a preinstalled kubectl binary from a trusted source or explicitly provide a trusted kubectl path.

Risk: Using insecure TLS options for credential material can expose kubeconfig contents.

Mitigation: Do not use --insecure for kubeconfig or other credential downloads.

## Reference(s):

- [Server-resolved source repository](https://github.com/yoshino-s/k8s-helper)
- [ClawHub skill page](https://clawhub.ai/yoshino-s/skills/k8s-helper)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May invoke kubectl and use local or cached kubeconfig and kubectl files when the user runs the provided wrapper.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
