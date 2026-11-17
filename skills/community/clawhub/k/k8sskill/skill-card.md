## Description:

Diagnoses Kubernetes cluster issues such as Pod crashes, deployment failures, service access problems, node health, storage failures, warning events, and related resource misconfigurations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magicczc](https://clawhub.ai/user/magicczc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to inspect Kubernetes clusters from natural-language requests and receive diagnostic findings with suggested remediation steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can over-collect sensitive Kubernetes Secret data during Secret analysis.

Mitigation: Use a dedicated read-only kubeconfig scoped to the namespaces being inspected, and avoid Secret analysis until namespace scoping and Secret caching are fixed.

Risk: Unsafe kubeconfig handling can expose broad cluster credentials.

Mitigation: Do not use cluster-admin credentials or store kubeconfig files inside the skill directory.

## Reference(s):

- [Analyzer Detailed Description](references/analyzers.md)
- [Troubleshooting Manual](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown diagnostic report; JSON output is available through the Python API.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can scope analysis by namespace and label selector; requires Kubernetes API access through kubeconfig.]

## Skill Version(s):

1.0.1 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
