## Description: <br>
KubeVPN is a cloud-native dev tool to connect a local machine to Kubernetes cluster networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wencaiwulue](https://clawhub.ai/user/wencaiwulue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to get KubeVPN command guidance for local development, debugging, cluster-network access, traffic interception, local workload simulation, and hot-reload workflows against Kubernetes clusters. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: KubeVPN workflows can change routing, proxy traffic, inject sidecars, run workload images locally, sync code, reset workloads, or uninstall cluster components. <br>
Mitigation: Use only authorized kube contexts, prefer non-production namespaces and header-scoped routing, and confirm the context, namespace, workload, and cleanup plan before running proxy, run, sync, reset, or uninstall commands. <br>
Risk: Kubernetes credentials, SSH details, tokens, passwords, or kubeconfig JSON can be exposed through command history or logs if supplied inline. <br>
Mitigation: Use least-privilege kube contexts and avoid placing secrets or kubeconfig JSON directly in commands, chat transcripts, shell history, or logs. <br>


## Reference(s): <br>
- [KubeVPN CLI Command Reference](references/commands.md) <br>
- [KubeVPN Architecture](references/architecture.md) <br>
- [KubeVPN install script](https://kubevpn.dev/install.sh) <br>
- [KubeVPN Helm repository](https://kubevpn.dev/helm) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Command guidance should be reviewed against the active kube context, namespace, workload, and cleanup requirements before execution.] <br>

## Skill Version(s): <br>
2.9.14 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
