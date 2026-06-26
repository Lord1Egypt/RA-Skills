## Description: <br>
Manage, deploy, monitor, and troubleshoot Kubernetes clusters with tools for multi-cluster control, resource monitoring, log aggregation, diagnostics, and Helm release operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kaiyuelv](https://clawhub.ai/user/kaiyuelv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and platform engineers use this skill to inspect Kubernetes clusters, review pod and node status, collect logs and events, diagnose common workload failures, and run Helm release actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may use live Kubernetes credentials and access cluster logs. <br>
Mitigation: Use a restricted kubeconfig and RBAC role, and limit access to clusters and namespaces the agent is intended to operate on. <br>
Risk: Helm install, upgrade, and rollback actions can change running workloads. <br>
Mitigation: Test changes against non-production clusters first, verify the active context and namespace, and review release names, chart versions, and values before execution. <br>
Risk: Dependency updates could change behavior in stricter environments. <br>
Mitigation: Use pinned or locked dependencies when deploying the skill in controlled or production workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/kaiyuelv/kubernetes-devops-toolkit) <br>
- [Publisher Profile](https://clawhub.ai/user/kaiyuelv) <br>
- [README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python examples, shell commands, configuration notes, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference kubeconfig contexts, namespaces, pod names, Helm releases, chart names, and diagnostic log excerpts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
