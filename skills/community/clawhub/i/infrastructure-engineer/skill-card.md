## Description:

云基础设施工程师技能库：Terraform 模块开发、基础设施变更安全审查、Kubernetes 可观测性、数据工程基础设施（IaC）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[skills-repo](https://clawhub.ai/user/skills-repo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill set to design reusable Terraform modules, review infrastructure plans, manage data infrastructure, and configure Kubernetes observability.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's instructions conflict over whether the agent may change live cloud infrastructure.

Mitigation: Before granting production write access, clarify the account, workspace, and permitted changes; use read-only credentials for review tasks.

Risk: Terraform plan and state exports may be exposed if committed or shared.

Mitigation: Keep exports out of commits and shared locations, and remove them when finished.

Risk: Global installer commands can use unreviewed versions or source revisions.

Mitigation: Review installer versions and source revisions before using global installation commands.

## Reference(s):

- [Terraform change safety playbook](references/terraform-change-safety.md)
- [Kubernetes observability playbook](references/kubernetes-observability.md)
- [Infrastructure as code module design playbook](references/iac-module-design.md)
- [Infrastructure review checklist](assets/infra-review-checklist.md)
- [Terraform plan risk script](scripts/tf_plan_risk.py)
- [Terraform module library listing](https://skills.sh/wshobson/agents/terraform-module-library)
- [Terraform diff analyzer listing](https://skills.sh/github/awesome-copilot/terraform-azurerm-set-diff-analyzer)
- [Kubernetes observability listing](https://skills.sh/dynatrace/dynatrace-for-ai/dt-obs-kubernetes)
- [Terraform data infrastructure listing](https://skills.sh/aradotso/data-skills/terraform-data-engineering-infrastructure)
- [ClawHub release page](https://clawhub.ai/skills-repo/skills/infrastructure-engineer)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown reports and guidance with Terraform/HCL, configuration examples, and shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes change review findings and recommendations; production changes require their scope and permissions to be clarified.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
