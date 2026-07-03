## Description: <br>
Deploys a YOLO training platform on Huawei Cloud with GPU ECS infrastructure managed through Terraform and helper scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to prepare and deploy a GPU-backed YOLO visual model training environment on Huawei Cloud, review Terraform variables and plans, verify the running service, and clean up provisioned resources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud access keys may be written to terraform.auto.tfvars.json on the local machine. <br>
Mitigation: Use short-lived or least-privilege Huawei Cloud credentials, avoid writing AK/SK values to the file unless explicitly intended, keep terraform.auto.tfvars.json local, and add it to ignore rules if generated. <br>
Risk: Terraform apply or destroy can create, modify, delete, or incur charges for Huawei Cloud GPU resources. <br>
Mitigation: Require a manual review of terraform plan and explicit user confirmation before apply or destroy, and verify billing parameters before deployment. <br>
Risk: Exposing the YOLO web UI or SSH broadly can create unnecessary network exposure. <br>
Mitigation: Use restricted CIDR ranges for SSH and TCP port 8001, avoid opening access to all addresses, and verify security group rules after deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huaweiclouddev/huawei-cloud-sac-yolo) <br>
- [Huawei Cloud YOLO solution page](https://www.huaweicloud.com/solution/implementations/quickly-build-a-yolo-training-platform.html) <br>
- [Huawei Cloud YOLO IAM reference](https://support.huaweicloud.com/yolo-aislt/yolo_04.html) <br>
- [Terraform template download](https://documentation-samples.obs.cn-north-4.myhuaweicloud.com/solution-as-code-publicbucket/solution-as-code-moudle/quickly-build-a-yolo-training-platform/quickly-build-a-yolo-training-platform.tf) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [IAM Policies](references/iam-policies.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Related Commands](references/related-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON outputs from helper scripts and Terraform] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or modify local Terraform working files, including terraform.auto.tfvars.json, and may guide Terraform apply or destroy after user confirmation.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
