## Description: <br>
Manage multiple Kubernetes clusters, switch contexts, and perform cross-cluster operations for comparison, lifecycle management, Helm, GitOps, and federation workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rohitg00](https://clawhub.ai/user/rohitg00) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, DevOps engineers, and platform teams use this skill to work across Kubernetes clusters, explicitly select contexts, compare environments, perform health checks, and manage Cluster API, Helm, GitOps, and federation operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact operations across multiple Kubernetes clusters, including production contexts. <br>
Mitigation: Use least-privileged kubeconfigs, make production read-only by default, always specify the intended context, and require explicit human approval for write actions. <br>
Risk: Cross-cluster workflows can expose or mishandle kubeconfigs, credentials, or Kubernetes secrets. <br>
Mitigation: Use separate credentials per environment, avoid copying raw secrets between clusters, and rely on sanitized kubeconfig views when reviewing access. <br>
Risk: Operations depend on external kubectl-mcp-server configuration and may be hard to audit if tooling is misconfigured. <br>
Mitigation: Verify kubectl-mcp-server configuration before use and enable audit logging for cluster access and cross-cluster changes. <br>


## Reference(s): <br>
- [Kubernetes Context Management](artifact/CONTEXT-SWITCHING.md) <br>
- [ClawHub release page](https://clawhub.ai/rohitg00/k8-multicluster) <br>
- [Publisher profile](https://clawhub.ai/user/rohitg00) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with inline Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational recommendations and command snippets; execution depends on the agent's Kubernetes, MCP, and cluster permissions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
