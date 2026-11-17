## Description:

KubeVPN helps agents provide guidance for connecting local machines to Kubernetes cluster networks, intercepting workload traffic, running workloads locally, and syncing code into cluster workloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wencaiwulue](https://clawhub.ai/user/wencaiwulue)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to get practical KubeVPN command guidance for local Kubernetes development, debugging remote workloads, selective traffic routing, cluster access through SSH jump hosts, and cleanup operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes a pipe-to-shell installation command.

Mitigation: Install KubeVPN through a trusted package manager or verified signed release instead of piping a remote script to a shell.

Risk: KubeVPN commands can make high-impact Kubernetes and Docker changes, including traffic interception, workload injection, and local privileged containers.

Mitigation: Use least-privilege kubeconfigs, prefer non-production namespaces, check injected or deployed resources before running commands, and avoid privileged local containers unless required.

Risk: Inline tokens, passwords, kubeconfigs, and SSH credentials can expose cluster or jump-host access.

Mitigation: Avoid inline secrets, prefer existing kubeconfig and SSH config references, and keep credentials out of prompts and command history.

Risk: Traffic interception can disrupt shared workloads when all inbound traffic is proxied to a local machine.

Mitigation: Use header-based routing where possible and run cleanup commands such as leave, disconnect, quit, reset, or uninstall after use.

## Reference(s):

- [KubeVPN CLI Command Reference](references/commands.md)
- [KubeVPN Architecture](references/architecture.md)
- [KubeVPN Helm Repository](https://kubevpn.dev/helm)
- [ClawHub kubevpn Skill Page](https://clawhub.ai/wencaiwulue/skills/kubevpn)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Kubernetes, Docker, Helm, SSH, and kubeconfig command options tailored to the user's cluster workflow.]

## Skill Version(s):

2.9.14 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
