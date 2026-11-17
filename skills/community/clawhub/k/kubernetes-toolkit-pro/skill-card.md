## Description:

Helps operations teams manage Kubernetes clusters with multi-cluster status workflows, policy governance, monitoring, GitOps, CRD lifecycle tasks, and disaster recovery guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, SREs, and enterprise operations teams use this skill to plan and execute Kubernetes management workflows across clusters, including policy checks, GitOps synchronization, monitoring, CRD management, and backup or recovery tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact Kubernetes changes such as deploy, enforce, CRD install, prune, self-heal, and backup operations.

Mitigation: Restrict kubeconfig contexts and API tokens to the minimum required clusters and namespaces, and require explicit confirmation before high-impact operations.

Risk: The artifact references scripts and requirements that are not included.

Mitigation: Verify any script path, dependency file, and command target before execution, and do not grant write access until the operational files are reviewed.

Risk: Broad activation wording may cause the skill to be used for sensitive cluster administration outside the intended scope.

Mitigation: Use it only for Kubernetes operations workflows and keep physical hardware, unrelated infrastructure, and unrestricted command execution out of scope.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/kubernetes-toolkit-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash and YAML examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Kubernetes command examples, configuration snippets, status summaries, logs, and remediation guidance.]

## Skill Version(s):

1.0.0 (source: evidence.json release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
