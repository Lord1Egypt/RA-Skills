## Description: <br>
Deploys the NewAPI LLM Gateway on Huawei Cloud with Terraform for unified large-model API gateway management, load balancing, and key rotation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to deploy, verify, and clean up a Huawei Cloud NewAPI LLM Gateway backed by ECS, VPC, EIP, EVS, Docker, and Terraform. It is intended for users who need a guided workflow with credential handling, plan review, and post-deployment validation. <br>

### Deployment Geography for Use: <br>
Huawei Cloud cn-north-4 region <br>

## Known Risks and Mitigations: <br>
Risk: Huawei Cloud access keys and generated Terraform variable files may expose credentials if copied into chat, logs, artifacts, or version control. <br>
Mitigation: Use a dedicated least-privilege IAM user, keep terraform.auto.tfvars.json out of logs and version control, never display its contents, and delete it after use. <br>
Risk: Terraform apply and destroy operations can create billable cloud resources or remove live infrastructure. <br>
Mitigation: Review terraform plan output, confirm costs and resource changes with the user before apply or destroy, and verify cleanup with Terraform state checks. <br>
Risk: The deployment exposes SSH and the NewAPI web interface on public network endpoints. <br>
Mitigation: Restrict public access where possible, review security group rules, and validate that only required ports are exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huaweiclouddev/huawei-cloud-sac-new-api) <br>
- [Huawei Cloud NewAPI LLM Gateway solution](https://www.huaweicloud.com/solution/implementations/building-a-newapi-llm-gateway.html) <br>
- [Terraform template](https://documentation-samples.obs.cn-north-4.myhuaweicloud.com/solution-as-code-publicbucket/solution-as-code-moudle/building-a-newapi-llm-gateway/building-a-newapi-llm-gateway.tf.json) <br>
- [CLI Installation Guide](references/cli-installation-guide.md) <br>
- [IAM Policies](references/iam-policies.md) <br>
- [Verification Method](references/verification-method.md) <br>
- [Acceptance Criteria](references/acceptance-criteria.md) <br>
- [Related Commands](references/related-commands.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Masks sensitive credential values, requires user confirmation before apply or destroy, and expects Terraform JSON outputs for deployment details.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
