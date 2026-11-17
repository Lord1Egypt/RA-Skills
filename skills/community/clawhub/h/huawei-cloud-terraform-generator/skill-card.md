## Description:

Generate Huawei Cloud Terraform configurations and execute deployment with user-guided approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to turn Huawei Cloud infrastructure goals into Terraform configurations, validate plans, and guide approved deployment steps. It is intended for workflows that need region-aware resource checks, credential handling, cost review, and user confirmation before applying changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent toward Terraform operations that create real Huawei Cloud resources and costs.

Mitigation: Use least-privilege credentials and review generated Terraform, plan output, and cost estimates before approving apply or destroy.

Risk: Generated network rules, terraform.tfvars values, kubeconfig files, cloud-init scripts, or systemd services may affect account security.

Mitigation: Review security group ports, sensitive configuration files, and startup/service scripts before deployment approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-terraform-generator)
- [Publisher profile](https://clawhub.ai/user/huaweicloudskill)
- [Terraform generation guide](artifact/reference/terraform-generation-guide.md)
- [Validation workflow](artifact/reference/validation-workflow.md)
- [Guardrails](artifact/reference/guardrails.md)
- [Huawei Cloud best practices](artifact/reference/Huawei-best-practices/Huawei-best-practices.md)
- [Huawei Cloud Terraform mirror](https://mirrors.huaweicloud.com/terraform/)
- [Huawei Cloud pricing calculator](https://www.huaweicloud.com/pricing.html#/calculator)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with Terraform files, shell commands, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate Terraform project files such as providers.tf, variables.tf, main.tf, terraform.tfvars, and README.md.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
