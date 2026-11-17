## Description: <br>
Kubernetes Toolkit Free helps individual developers and small teams create, inspect, update, and troubleshoot common Kubernetes resources such as Pods, Services, Deployments, ConfigMaps, and Secrets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and engineers use this skill to manage personal development and small-team Kubernetes clusters, including application deployment, resource queries, namespace management, configuration handling, and basic troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change or delete live Kubernetes resources when the agent has access to a kubeconfig. <br>
Mitigation: Use a least-privilege kubeconfig, verify the active context and namespace before commands, and require manual approval for delete, scale, rollout, and other mutating operations. <br>
Risk: Kubernetes Secret and kubeconfig workflows may expose credentials or sensitive cluster access details. <br>
Mitigation: Avoid inline secrets, redact logs and command output, and keep kubeconfig access scoped to the minimum namespaces and verbs required. <br>
Risk: Generated commands may target the wrong namespace, context, or resource in shared clusters. <br>
Mitigation: Review proposed commands before execution and explicitly set context, namespace, and resource names for each operation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/kubernetes-toolkit-free) <br>
- [Skill homepage](https://skillhub.cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and structured status, result, and log responses.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires kubeconfig-backed cluster access; the free edition describes basic resource management for up to five namespaces and excludes monitoring and policy governance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
