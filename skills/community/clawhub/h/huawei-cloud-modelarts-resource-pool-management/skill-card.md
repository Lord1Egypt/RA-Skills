## Description:

Manage Huawei Cloud ModelArts dedicated resource pools and node pools across their lifecycle, including nodes, networks, tags, plugins, workloads, scheduled events, and pricing guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud administrators and developers use this skill to inspect and manage ModelArts dedicated resource pools and related resources through the hcloud CLI. It requires confirmation for write operations and cost review before chargeable changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The pricing helper may misstate costs.

Mitigation: Wait for fixes to its input handling and total calculation before running it, and verify costs independently before chargeable changes.

Risk: Crafted region input may be executed as code by the pricing helper.

Mitigation: Do not run the helper until its input handling is fixed.

Risk: Automatic payment may be enabled without being clearly explained.

Mitigation: Explicitly choose the automatic-payment setting and make it clear before proceeding.

Risk: Deleting resources may affect workloads or backups.

Mitigation: Review affected workloads and backups before approving each deletion.

Risk: External installer contents and live cloud behavior have not been verified.

Mitigation: Verify installer integrity and inspect command responses and resulting cloud changes before continuing.

## Reference(s):

- [ClawHub release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-modelarts-resource-pool-management)
- [hcloud CLI quick start](https://support.huaweicloud.com/qs-hcli/hcli_02_003.html)
- [ModelArts API Explorer](https://console.huaweicloud.com/apiexplorer/#/openapi/ModelArts)
- [CLI command examples](references/cli-command-examples.md)
- [IAM policies](references/iam-policies.md)
- [Pricing inquiry guidance](references/pricing-inquiry.md)
- [Known issues](references/known-issues.md)

## Skill Output:

**Output Type(s):** [Text, API calls, Shell commands, Configuration guidance]

**Output Format:** [Markdown with shell command examples and API results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands and guidance depend on the selected region, resource, and requested operation.]

## Skill Version(s):

1.0.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
