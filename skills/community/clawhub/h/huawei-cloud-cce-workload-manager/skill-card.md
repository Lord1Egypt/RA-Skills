## Description: <br>
Huawei Cloud CCE/UCS workload lifecycle management skill using hcloud CLI for kubeconfig acquisition and kubectl for Kubernetes resource operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pintudeyudi](https://clawhub.ai/user/pintudeyudi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to acquire Huawei Cloud CCE/UCS kubeconfigs and manage Kubernetes workloads, services, scaling, namespaces, storage, configuration, and pod observability with hcloud and kubectl. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad cluster-changing operations and credential-generating workflows. <br>
Mitigation: Scope Huawei Cloud IAM and Kubernetes RBAC to specific clusters and namespaces, and require explicit confirmation before deletes, rollbacks, scale changes, pod exec, port-forwarding, PVC deletion, namespace deletion, or production operations. <br>
Risk: Generated kubeconfig files grant cluster access and should be treated as credentials. <br>
Mitigation: Protect kubeconfig files, use short validity durations where possible, and avoid exposing credential material in commands, logs, or conversation. <br>
Risk: Inline secret or password examples can expose sensitive values if copied into commands or manifests. <br>
Mitigation: Avoid inline passwords, prefer secret-management workflows, and review Secret manifests before applying them. <br>


## Reference(s): <br>
- [CCE Workload API Guide](references/cce-workload-api-guide.md) <br>
- [IAM Policies](references/iam-policies.md) <br>
- [Kubeconfig Acquisition](references/task-kubeconfig-acquisition.md) <br>
- [kubectl Setup](references/task-kubectl-setup.md) <br>
- [Deployment Management](references/task-deployment-management.md) <br>
- [StatefulSet and DaemonSet Management](references/task-statefulset-daemonset-management.md) <br>
- [Job and CronJob Management](references/task-job-cronjob-management.md) <br>
- [HPA Scaling](references/task-hpa-scaling.md) <br>
- [Service and Ingress](references/task-service-ingress.md) <br>
- [Config and Secret Storage](references/task-config-secret-storage.md) <br>
- [Namespace Management](references/task-namespace-management.md) <br>
- [Pod Observability](references/task-pod-observability.md) <br>
- [Common Pitfalls](references/common-pitfalls.md) <br>
- [Verification Method](references/verification-method.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and Kubernetes YAML/JSON snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose cluster-changing hcloud and kubectl commands that require operator review before execution.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
