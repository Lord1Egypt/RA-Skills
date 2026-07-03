## Description: <br>
Generates Huawei Cloud Terraform configurations, validates them through Terraform plan, and applies deployments only after user-guided approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[huaweiclouddev](https://clawhub.ai/user/huaweiclouddev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and cloud engineers use this skill to translate Huawei Cloud infrastructure goals into Terraform files, validation commands, and deployment guidance. It supports guided creation of compute, network, database, storage, load balancing, DNS, monitoring, and related cloud resources with explicit plan and apply approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated Terraform can create paid, security-sensitive, or long-running Huawei Cloud resources. <br>
Mitigation: Require manual review of every Terraform plan and explicit approval before running terraform apply. <br>
Risk: Credential or secret handling can expose AK/SK values, passwords, tokens, or private keys if written into prompts, provider blocks, or committed files. <br>
Mitigation: Use environment variables for Huawei Cloud AK/SK, avoid plaintext secrets in Terraform variables where possible, and review terraform.tfvars before storing or sharing generated files. <br>
Risk: Region-specific resource specifications, images, flavors, zones, or prices can be wrong if generated from assumptions. <br>
Mitigation: Verify each target-region specification and price through reliable lookup or user-provided evidence before writing Terraform. <br>
Risk: Bundled examples may include provisioners or remote execution patterns that run commands on local or remote systems. <br>
Mitigation: Review local-exec and remote-exec provisioners before validation or apply, and remove execution steps that are not required for the approved deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/huaweiclouddev/skills/huawei-cloud-terraform-generator) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Guardrails](artifact/reference/guardrails.md) <br>
- [Terraform generation guide](artifact/reference/terraform-generation-guide.md) <br>
- [Validation workflow](artifact/reference/validation-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Files, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown guidance with Terraform HCL, bash commands, and generated workspace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates providers.tf, variables.tf, main.tf, terraform.tfvars, and README.md; avoids outputs.tf and Terraform output blocks.] <br>

## Skill Version(s): <br>
0.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
