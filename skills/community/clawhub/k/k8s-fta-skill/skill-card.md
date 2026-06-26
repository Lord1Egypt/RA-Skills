## Description: <br>
Troubleshoots Kubernetes and k3s cluster issues with fault tree analysis, proposing or executing kubectl checks and fixes for Pods, services, RBAC, DNS, storage, autoscaling, API server, and related failures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yejinlei](https://clawhub.ai/user/yejinlei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to investigate Kubernetes and k3s incidents, identify likely causes, and prepare or run kubectl-based remediation with confirmation for changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can operate against Kubernetes clusters and may suggest or execute changes that disrupt workloads or control-plane components. <br>
Mitigation: Use a deliberately selected, least-privilege kubeconfig and namespace, avoid production unless reviewed internally, and require explicit approval before patch, delete, exec, RBAC, certificate, or etcd actions. <br>
Risk: Automated fixes may be incorrect for the target cluster or incident context. <br>
Mitigation: Review every proposed command before execution, prefer read-only diagnostics first, and keep rollback or restore steps available for modifications. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and troubleshooting recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include kubectl commands, diagnosis summaries, fix recommendations, and validation steps.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
