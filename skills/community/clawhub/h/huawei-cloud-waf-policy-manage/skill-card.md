## Description:

Import WAF protection policies from JSON files exported by huawei-cloud-waf-policy-query, supporting creation of new policies or overwriting existing ones.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud security engineers and platform operators use this skill to migrate, copy, or synchronize Huawei Cloud WAF protection policies from JSON exports. It guides review, creation, overwrite, rule recreation, and post-import verification workflows for managed WAF policies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live creation, update, overwrite, and deletion of Huawei Cloud WAF policies and rules.

Mitigation: Use a test account or non-production WAF policy first, export or back up existing policies before overwrite, and require explicit confirmation before any deletion or destructive overwrite.

Risk: The provided IAM examples include broad WAF mutation and deletion authority.

Mitigation: Avoid wildcard IAM policies for production use and grant only the exact query, create, update, or delete permissions needed for the chosen workflow.

Risk: Incorrect JSON inputs or CLI parameter mappings can create incomplete or misconfigured WAF policies.

Mitigation: Validate that JSON was exported by huawei-cloud-waf-policy-query, review planned commands before execution, run a small-scale import first, and verify results with read-only WAF queries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-waf-policy-manage)
- [KooCLI installation and configuration guide](artifact/references/cli-installation-guide.md)
- [Huawei Cloud KooCLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [IAM policies for WAF policy management](artifact/references/iam-policies.md)
- [Verification methods](artifact/references/verification-method.md)
- [Data flow diagram](artifact/references/dataflow-diagram.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides live Huawei Cloud WAF CLI operations and requires user confirmation before write or delete actions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
