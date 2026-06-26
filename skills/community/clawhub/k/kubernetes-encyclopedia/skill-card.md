## Description: <br>
Provides a documentation-first workflow for Kubernetes questions, troubleshooting, command planning, cluster operations, and resource behavior using official docs plus a local workspace cache. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kklouzal](https://clawhub.ai/user/kklouzal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to answer Kubernetes-specific questions, plan kubectl or manifest work, troubleshoot cluster behavior, and preserve useful documentation and operational notes in a local cache. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch Kubernetes documentation from the network. <br>
Mitigation: Use it where access to official Kubernetes documentation is acceptable and review fetched material before relying on it. <br>
Risk: The skill can create or update a local .Kubernetes-Encyclopedia workspace containing cached docs and operational notes. <br>
Mitigation: Review the cache location, keep secrets and kubeconfig material out of notes, and use it only in workspaces where local documentation files are acceptable. <br>
Risk: Suggested kubectl commands or manifest changes could affect workloads, access, traffic, storage, or cluster reachability if executed without review. <br>
Mitigation: Review proposed commands and manifests before execution, prefer read-only inspection first, and apply extra review for cluster-wide, RBAC, ingress, storage, and node changes. <br>


## Reference(s): <br>
- [Kubernetes Documentation](https://kubernetes.io/docs/home/) <br>
- [Kubernetes Deployment Documentation](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/) <br>
- [Workflow Reference](references/workflow.md) <br>
- [Cache Layout Reference](references/cache-layout.md) <br>
- [Topic Map Reference](references/topic-map.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and file-path guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update workspace-local Kubernetes documentation cache and notes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
