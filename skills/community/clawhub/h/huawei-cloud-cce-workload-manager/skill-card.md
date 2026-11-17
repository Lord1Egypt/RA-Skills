## Description:

Huawei Cloud CCE/UCS workload lifecycle management skill using hcloud CLI for kubeconfig acquisition and kubectl for Kubernetes resource operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pintudeyudi](https://clawhub.ai/user/pintudeyudi)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to acquire Huawei Cloud CCE or UCS kubeconfigs and manage Kubernetes workloads, networking, configuration, storage, namespaces, and observability with hcloud CLI and kubectl.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires authority to obtain kubeconfigs and manage Huawei Cloud CCE or UCS Kubernetes resources.

Mitigation: Use a narrowly scoped IAM user, align Kubernetes RBAC with the intended task, prefer short-lived kubeconfigs, and avoid cluster-admin permissions by default.

Risk: Kubeconfigs, Huawei Cloud AK/SK credentials, and Kubernetes Secrets can be exposed through commands, transcripts, logs, or files.

Mitigation: Use environment variables or masked credential configuration, never paste real secrets into chat or command arguments, store kubeconfig files with restricted permissions, and remove temporary kubeconfigs after use.

Risk: Generated kubectl commands can change or delete live workloads, namespaces, services, storage, or autoscaling behavior.

Mitigation: Review commands before execution, require explicit user confirmation for destructive actions, target namespaces explicitly, and verify rollouts, RBAC, and cluster connectivity before write operations.

Risk: Tool setup and UCS federation access depend on external binaries, correct regions, and VPCEP or network reachability.

Mitigation: Verify kubectl downloads and versions, confirm hcloud region and cluster identifiers, and validate UCS federation DNS or VPCEP access before troubleshooting workload behavior.

## Reference(s):

- [CCE Workload Manager API Reference Guide](references/cce-workload-api-guide.md)
- [Common Pitfalls & Solutions](references/common-pitfalls.md)
- [IAM Policies](references/iam-policies.md)
- [Task: Kubeconfig Acquisition](references/taREDACTED-SECRET.md)
- [Task: kubectl Setup](references/task-kubectl-setup.md)
- [Task: Deployment Management](references/taREDACTED-SECRET.md)
- [Task: StatefulSet/DaemonSet Management](references/taREDACTED-SECRET.md)
- [Task: Job/CronJob Management](references/taREDACTED-SECRET.md)
- [Task: HPA Scaling](references/task-hpa-scaling.md)
- [Task: Service & Ingress Management](references/task-service-ingress.md)
- [Task: ConfigMap, Secret, and PVC Storage](references/taREDACTED-SECRET.md)
- [Task: Namespace Management](references/taREDACTED-SECRET.md)
- [Pod Observability](references/task-pod-observability.md)
- [Verification Method - CCE Workload Manager Skill](references/verification-method.md)
- [Huawei Cloud CCE Documentation](https://support.huaweicloud.com/cce/index.html)
- [Huawei Cloud UCS Documentation](https://support.huaweicloud.com/ucs/index.html)
- [hcloud CLI Documentation](https://support.huaweicloud.com/cli/index.html)
- [Huawei Cloud API Explorer](https://apiexplorer.developer.huaweicloud.com/)
- [Official kubectl Installation Guide](https://kubernetes.io/docs/tasks/tools/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and YAML or JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose commands for live Kubernetes resources; the agent should keep kubeconfig paths explicit and request confirmation before destructive operations.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
