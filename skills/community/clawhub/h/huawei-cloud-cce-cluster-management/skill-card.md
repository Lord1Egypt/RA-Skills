## Description: <br>
Huawei Cloud CCE cluster management skill for creating, deleting, hibernating, awakening, querying, and administering CCE clusters, nodes, node pools, addons, EIP bindings, and kubeconfig access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud operations engineers use this skill to administer Huawei Cloud CCE Kubernetes infrastructure, including cluster lifecycle operations, node and node pool management, addon management, network prerequisites, and kubeconfig retrieval. <br>

### Deployment Geography for Use: <br>
Huawei Cloud regions listed in the skill documentation, primarily China and Asia-Pacific regions. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change live Huawei Cloud CCE infrastructure, including delete, resize, hibernate, drain, addon, and EIP operations. <br>
Mitigation: Use least-privilege Huawei credentials, test in non-production accounts first, and require explicit human approval before create, delete, resize, drain, addon, or EIP operations. <br>
Risk: Kubeconfig output, Huawei credentials, and node passwords are sensitive and could grant access to clusters or cloud resources. <br>
Mitigation: Treat kubeconfig and credential values as secrets, avoid storing them in logs or shared files, and prefer environment or secret-manager injection for credentials. <br>
Risk: Cluster deletion, hibernation, node drain, and node pool changes can disrupt workloads or reduce service capacity. <br>
Mitigation: Preview dangerous operations before confirmation, schedule disruptive actions during maintenance windows, and verify replicas, backups, and cluster health before proceeding. <br>


## Reference(s): <br>
- [Cluster Management Task Details](references/task-cluster-management.md) <br>
- [Node Pool Management Task Details](references/task-nodepool-management.md) <br>
- [Node Management Task Details](references/task-node-management.md) <br>
- [CCE IAM Permission Configuration](references/iam-policies.md) <br>
- [Feature Verification Steps](references/verification-method.md) <br>
- [Common Troubleshooting Issues](references/troubleshooting.md) <br>
- [CCE SDK API Reference](references/cce-api-guide.md) <br>
- [Cluster Creation Parameter Reference](references/cce-cluster-parameters.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON responses with status, data, message, and warning fields; Markdown guidance with shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Kubeconfig output and credential-related values should be handled as secrets; dangerous operations may return preview warnings until confirm=true is supplied.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
