## Description:

Queries Huawei Cloud resources across regions and services, then converts the results into resource inventories and marker-table workbooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud engineers and operations teams use it to inventory Huawei Cloud resources, collect architecture data, reconcile accounts, and prepare migration planning. It produces point-in-time findings scoped to the regions and services queried.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates this skill suspicious because it reports serious risks around cloud credentials, automatic setup, data handling, and incomplete analysis, though the findings do not establish malicious intent.

Mitigation: The scanner's recommendation is not to install. Before considering it, have a trusted reviewer examine the partially analyzed script and address the reported TLS, credential persistence and exposure, automatic package installation, secret export, and output deletion risks.

## Reference(s):

- [CLI Installation Guide](artifact/references/cli-installation-guide.md)
- [IAM Policies](artifact/references/iam-policies.md)
- [Verification Method](artifact/references/verification-method.md)
- [Service Coverage](artifact/references/service-coverage.md)
- [Acceptance Criteria](artifact/references/acceptance-criteria.md)
- [Resource Ontology](artifact/references/semantic/resource-ontology.yml)
- [ClawHub release page](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-architecture-resource-archive)
- [KooCLI download](https://obs.cn-north-4.myhuaweicloud.com/hcloud/cli/latest/hcloud.zip)

## Skill Output:

**Output Type(s):** [JSON, Excel workbook, Text inventory summaries, Configuration guidance]

**Output Format:** [Resource records in JSON, a marker-table workbook in Excel, and concise briefing text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Point-in-time results scoped to the account, regions, and services queried; report partial coverage explicitly.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
