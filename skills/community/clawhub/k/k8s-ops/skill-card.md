## Description: <br>
Kubernetes operations plugin - 32 tools for cluster management, monitoring, troubleshooting, and security auditing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cn-big-cabbage](https://clawhub.ai/user/cn-big-cabbage) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to manage, monitor, troubleshoot, and audit Kubernetes clusters through OpenClaw with kubectl-backed operational workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can exercise real Kubernetes operational authority, including write operations against live clusters. <br>
Mitigation: Use a dedicated least-privilege kubeconfig, verify the current context and namespace before write actions, and avoid cluster-admin except for explicit break-glass cases. <br>
Risk: Remote manifests, rollout, scale, restart, namespace, and exec workflows may cause unintended production changes. <br>
Mitigation: Review remote manifests and proposed kubectl operations before applying them, and test changes in non-production environments where possible. <br>
Risk: SSH host configuration may expose sensitive access paths or credentials. <br>
Mitigation: Configure only trusted hosts, prefer SSH key authentication, and avoid storing raw SSH passwords in plugin configuration. <br>


## Reference(s): <br>
- [K8s Ops Agent Homepage](https://github.com/CN-big-cabbage/k8s-ops-agent) <br>
- [Kubernetes Documentation](https://kubernetes.io/docs/) <br>
- [Kubernetes Issues](https://github.com/kubernetes/kubernetes/issues) <br>
- [Kubernetes Discussion Forum](https://discuss.kubernetes.io/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Text and JSON details, with documentation examples in Markdown containing bash and YAML snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires kubectl, a valid kubeconfig, and appropriate cluster permissions.] <br>

## Skill Version(s): <br>
2.1.1 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
