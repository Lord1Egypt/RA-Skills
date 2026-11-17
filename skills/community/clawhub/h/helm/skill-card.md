## Description:

Create, lint, template, and package Kubernetes Helm charts with checks. Use when scaffolding charts, linting templates, or packaging chart releases.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to scaffold, inspect, lint, template, package, and manage Helm charts and Kubernetes release information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read live Kubernetes release data through Helm commands such as list, status, values, history, and diff.

Mitigation: Use a least-privilege kubeconfig and namespace scoped to the intended cluster before running cluster-reading commands.

Risk: The rollback command can change a live Kubernetes release.

Mitigation: Confirm the target cluster, namespace, release, and revision outside automation before running rollback.

Risk: The helper prints a curl-to-bash Helm install command when Helm is missing.

Mitigation: Verify Helm installation instructions independently before executing remote installation commands.

## Reference(s):

- [Helm install documentation](https://helm.sh/docs/intro/install/)
- [BytesAgain](https://bytesagain.com)
- [ClawHub skill page](https://clawhub.ai/xueyetianya/skills/helm)
- [Publisher profile](https://clawhub.ai/user/xueyetianya)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and Helm command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local chart scaffolds, packaged chart archives, and a helper log under the user's local data directory when its shell script is run.]

## Skill Version(s):

3.0.1 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
