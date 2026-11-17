## Description:

Query Huawei Cloud WAF protection policy lists and detailed configuration for selected policies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, cloud security engineers, and operations teams use this skill to inspect Huawei Cloud WAF protection policies, enabled modules, and rule details through the hcloud CLI without creating, modifying, or deleting cloud resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Detailed WAF configuration, IP groups, value lists, hostnames, and project metadata may be displayed or saved locally.

Mitigation: Require explicit user consent before exporting results, use a user-confirmed path, and handle saved JSON files as sensitive security configuration.

Risk: The skill includes an hcloud CLI language configuration command that can persistently change local CLI settings.

Mitigation: Run the CLI language configuration change only when the user wants that persistent hcloud setting changed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-waf-policy-query)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown tables and explanations with inline shell commands, plus optional JSON exports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save detailed WAF policy query results as local JSON files after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
