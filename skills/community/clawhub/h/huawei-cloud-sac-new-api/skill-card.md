## Description:

Deploys a NewAPI LLM Gateway on Huawei Cloud with Terraform for multi-model API management, load balancing, key rotation, and usage statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to prepare, review, deploy, verify, and clean up a Huawei Cloud NewAPI LLM Gateway deployment using Terraform and helper scripts.

### Deployment Geography for Use:

Huawei Cloud cn-north-4 only

## Known Risks and Mitigations:

Risk: The skill can guide Terraform operations that create, modify, or destroy Huawei Cloud infrastructure.

Mitigation: Use a least-privilege Huawei Cloud IAM user, review the Terraform plan, and require explicit confirmation before apply or destroy.

Risk: The workflow downloads a remote Terraform template before deployment.

Mitigation: Inspect and verify the downloaded template before running Terraform init, plan, or apply.

Risk: Terraform credentials may be materialized locally in terraform.auto.tfvars.json.

Mitigation: Keep cloud credentials out of shared workspaces and conversation context, never commit the file, and remove terraform.auto.tfvars.json after use.

Risk: Deployed SSH and web access can expose the ECS instance and NewAPI interface.

Mitigation: Restrict SSH and web access to trusted IP ranges and verify security group rules during review.

Risk: The security evidence warns about an unsafe Playwright npx fallback.

Mitigation: Avoid the fallback unless the package identity and version are pinned and reviewed.

## Reference(s):

- [CLI Installation Guide](references/cli-installation-guide.md)
- [IAM Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Related Commands](references/related-commands.md)
- [Huawei Cloud Building a NewAPI LLM Gateway](https://www.huaweicloud.com/solution/implementations/building-a-newapi-llm-gateway.html)
- [Huawei Cloud SAC Terraform Template](https://documentation-samples.obs.cn-north-4.myhuaweicloud.com/solution-as-code-publicbucket/solution-as-code-moudle/building-a-newapi-llm-gateway/building-a-newapi-llm-gateway.tf.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-oriented script and Terraform outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides Terraform plan, apply, verification, output review, and cleanup; generated credential files must stay local and out of conversation context.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
