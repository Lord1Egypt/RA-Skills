## Description:

Kubernetes documentation-first workflow for Kubernetes-specific questions, troubleshooting, command planning, cluster operations, workload and resource behavior, networking, storage, scheduling, security, and diagnostics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kklouzal](https://clawhub.ai/user/kklouzal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to answer Kubernetes-specific questions, plan kubectl and manifest work, troubleshoot cluster behavior, and preserve local operational notes while grounding guidance in official Kubernetes documentation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may fetch official Kubernetes documentation and create a .Kubernetes-Encyclopedia directory in the current workspace.

Mitigation: Use it where outbound access to kubernetes.io and workspace-local cache writes are acceptable, and treat cached copies as convenience material.

Risk: Workspace notes could accidentally include sensitive cluster details if users record them too specifically.

Mitigation: Do not store plaintext credentials, API keys, kubeconfigs, bearer tokens, private URLs, or full access details in notes or inventory files.

Risk: Kubernetes guidance or command plans can affect workloads, access, traffic, storage, policy, or cluster reachability.

Mitigation: Check the relevant official documentation and inspect live state before high-impact Kubernetes changes, and avoid acting when uncertainty remains.

Risk: The documentation cache helper has noted redirect and response-size bounds to review for tightly controlled network environments.

Mitigation: Review and harden cache_doc.py network behavior before deployment in restricted or highly regulated environments.

## Reference(s):

- [Kubernetes Documentation](https://kubernetes.io/docs/home/)
- [Kubernetes Encyclopedia Workflow](references/workflow.md)
- [Kubernetes Topic Map](references/topic-map.md)
- [Kubernetes Encyclopedia Cache Layout](references/cache-layout.md)
- [ClawHub Skill Page](https://clawhub.ai/kklouzal/skills/kubernetes-encyclopedia)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands, configuration snippets, and workspace notes when appropriate]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create .Kubernetes-Encyclopedia workspace files and cached Kubernetes documentation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
