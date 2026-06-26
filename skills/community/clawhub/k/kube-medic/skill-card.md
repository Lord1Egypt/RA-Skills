## Description: <br>
Kubernetes Cluster Triage & Diagnostics - instant AI-powered incident triage via kubectl. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tkuehnl](https://clawhub.ai/user/tkuehnl) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
SREs, platform engineers, and on-call responders use kube-medic to inspect Kubernetes cluster health, investigate failing pods or deployments, and produce triage reports with recommended remediation steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can inspect Kubernetes state and pod logs through the active kubeconfig, which may expose operational or sensitive application data. <br>
Mitigation: Use a read-only or namespace-scoped RBAC role, verify the active kubectl context before running diagnostics, and restrict pod log access where logs may contain sensitive data. <br>
Risk: Optional confirm-write commands can change cluster state and affect workload availability. <br>
Mitigation: Approve confirm-write commands only after checking the exact cluster, namespace, resource, command, and expected availability impact. <br>


## Reference(s): <br>
- [ClawHub kube-medic release](https://clawhub.ai/tkuehnl/kube-medic) <br>
- [Kubernetes kubectl tools documentation](https://kubernetes.io/docs/tasks/tools/) <br>
- [Kubernetes Metrics Server release manifest](https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml) <br>
- [kube-medic security policy](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Structured JSON from the tool, presented by the agent as Markdown triage reports with tables, timelines, and command blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires kubectl, jq, kubeconfig access, and metrics-server for resource metrics; diagnostic output can include pod logs.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
