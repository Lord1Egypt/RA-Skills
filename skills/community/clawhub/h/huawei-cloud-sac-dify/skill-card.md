## Description:

Deploys the Dify LLM application development platform on Huawei Cloud ECS using Terraform.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers deploying Dify on Huawei Cloud use the skill to review solution details and configuration, provision infrastructure with Terraform, verify access, and clean up resources.

### Deployment Geography for Use:

Huawei Cloud regions in China, Southeast Asia, and Turkey (including cn-north-4, ap-southeast-1, and tr-west-1).

## Known Risks and Mitigations:

Risk: Browser automation may accept website agreements automatically.

Mitigation: Remove automatic agreement clicks and require user review and consent before accepting an agreement.

Risk: Huawei Cloud credentials are stored in a local Terraform variables file and can remain on disk until teardown succeeds.

Mitigation: Use a private owner-only work directory and a restricted IAM identity; never expose credentials in chat or output, and delete the credentials file after successful teardown.

Risk: Downloaded templates and dependency versions may be unverified.

Mitigation: Review downloaded templates and dependency versions, then inspect and approve the Terraform plan before applying changes.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-sac-dify)
- [Huawei Cloud Dify solution](https://www.huaweicloud.com/solution/implementations/building-a-dify-llm-application-development-platform.html)
- [Huawei Cloud Terraform template](https://documentation-samples.obs.cn-north-4.myhuaweicloud.com/solution-as-code-publicbucket/solution-as-code-moudle/flexus/dify-ecs.tf)
- [IAM Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [CLI Installation Guide](references/cli-installation-guide.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Terraform configuration, Configuration guidance]

**Output Format:** [Markdown guidance, shell commands, Terraform configuration, and JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cloud deployment instructions and sensitive configuration guidance; credentials must not be printed.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
