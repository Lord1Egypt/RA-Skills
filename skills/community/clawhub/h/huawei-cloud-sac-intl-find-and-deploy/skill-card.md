## Description:

Finds Huawei Cloud international SAC solutions in the live catalog and, after user confirmation, deploys selected Terraform templates with verification and cleanup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud engineers use this skill to find Huawei Cloud international Solution as Code offerings and deploy a selected solution with Terraform after reviewing the region, credentials, variables, and plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional quality CLI may be installed automatically, and its telemetry fields and destination are unclear.

Mitigation: Ask before installing it and explain its telemetry fields and destination; keep reporting disabled when requested, noting that this does not prevent installation.

Risk: A downloaded Terraform template can create cloud resources and incur charges, and live templates are outside the supplied file review.

Mitigation: Review the selected template and Terraform plan, verify variables and region, and require explicit user confirmation before apply.

Risk: Cloud access keys and temporary security tokens are sensitive.

Mitigation: Use short-lived, least-privilege credentials through environment variables; never request or display them in chat.

## Reference(s):

- [Huawei Cloud SAC public catalog](https://documentation-samples-5.obs.ap-southeast-1.myhuaweicloud.com/solution-as-code-publicbucket/solution-as-code-module/sac_intl.json)
- [CLI Installation Guide](artifact/references/cli-installation-guide.md)
- [IAM Policies](artifact/references/iam-policies.md)
- [Verification Method](artifact/references/verification-method.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)
- [Terraform Installation](https://developer.hashicorp.com/terraform/install)

## Skill Output:

**Output Type(s):** [Text, JSON, Files, Code, Shell commands, Configuration instructions, Guidance]

**Output Format:** [JSON catalog results, Terraform configuration files, and Markdown guidance with shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Catalog results are fetched live. Deployment requires explicit selection and confirmation; credential values should remain outside chat.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
