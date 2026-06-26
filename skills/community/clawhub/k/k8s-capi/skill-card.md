## Description: <br>
Cluster API lifecycle management for provisioning, scaling, and upgrading Kubernetes clusters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rohitg00](https://clawhub.ai/user/rohitg00) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and platform engineers use this skill to manage Kubernetes Cluster API resources, including provisioning clusters, inspecting machines and deployments, scaling worker nodes, upgrading clusters, obtaining kubeconfigs, and troubleshooting cluster health. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mutating Cluster API examples can change cluster availability, capacity, provider resources, or cost. <br>
Mitigation: Verify the kubeconfig context, namespace, target cluster, provider, manifest, and intended impact before applying or scaling resources. <br>
Risk: Retrieved kubeconfigs can grant access to workload clusters. <br>
Mitigation: Treat kubeconfig output as secret material and avoid exposing it in logs, chat transcripts, shared files, or other public outputs. <br>


## Reference(s): <br>
- [Kubernetes Skills on ClawHub](https://clawhub.ai/rohitg00/k8s-capi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Kubernetes tool calls, manifest examples, and workflow steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include kubeconfig retrieval guidance and Kubernetes manifest examples; users should handle credentials as secrets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
