## Description:

Deploys a GPU-accelerated YOLO training platform on Huawei Cloud with Terraform-managed ECS, networking, storage, backup, and verification guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to deploy, review, verify, and clean up a Huawei Cloud GPU ECS environment for YOLO model training with Terraform.

### Deployment Geography for Use:

Global; the deployment workflow itself supports only Huawei Cloud cn-north-4.

## Known Risks and Mitigations:

Risk: The skill can require broad Huawei Cloud permissions for infrastructure creation and deletion.

Mitigation: Use a limited IAM user where possible, avoid Tenant Administrator unless required, inspect terraform plan carefully, and require explicit intent before apply or destroy.

Risk: The workflow can write Huawei Cloud access keys to a local terraform.auto.tfvars.json file.

Mitigation: Keep the tfvars file local and out of source control, prefer short-lived or tightly scoped AK/SK credentials, and do not expose credentials in chat or generated output.

Risk: The deployed YOLO UI requires an ingress rule for TCP port 8001.

Mitigation: Add the rule manually after deployment and restrict the CIDR to the user's own IP or another narrow trusted range.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-sac-yolo)
- [Huawei Cloud YOLO solution page](https://www.huaweicloud.com/solution/implementations/quickly-build-a-yolo-training-platform.html)
- [Huawei Cloud YOLO IAM support documentation](https://support.huaweicloud.com/yolo-aislt/yolo_04.html)
- [Huawei Cloud YOLO Terraform template](https://documentation-samples.obs.cn-north-4.myhuaweicloud.com/solution-as-code-publicbucket/solution-as-code-moudle/quickly-build-a-yolo-training-platform/quickly-build-a-yolo-training-platform.tf)
- [CLI Installation Guide](references/cli-installation-guide.md)
- [IAM Policies](references/iam-policies.md)
- [Verification Method](references/verification-method.md)
- [Acceptance Criteria](references/acceptance-criteria.md)
- [Related Commands](references/related-commands.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Terraform workflow guidance and helper-script outputs; deployment changes require explicit user confirmation.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
