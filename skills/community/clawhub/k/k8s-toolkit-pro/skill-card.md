## Description:

K8s运维专业版 helps enterprise Kubernetes operations teams diagnose cluster health, plan fixes, tune performance, review security compliance, and manage multiple clusters through agent-guided workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Kubernetes operators, platform engineers, and SRE teams use this skill to triage production and non-production clusters, generate diagnostic reports, review remediation plans, and prepare configuration or shell-command workflows for cluster maintenance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may propose powerful Kubernetes commands or auto-fix actions against production clusters.

Mitigation: Use least-privilege kubeconfig contexts, require dry-run previews, and obtain explicit approval before applying any cluster change.

Risk: Broad triggers and unsupported safety claims can make automation boundaries unclear.

Mitigation: Review the skill before installation, verify generated commands manually, and avoid scheduled automation or webhooks until the implementation and command boundaries are confirmed.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/thcjp/skills/k8s-toolkit-pro)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline bash and YAML code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include diagnostic summaries, remediation recommendations, compliance findings, operational runbooks, and commands that require human review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
