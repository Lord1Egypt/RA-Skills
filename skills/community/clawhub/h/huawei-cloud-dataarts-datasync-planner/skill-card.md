## Description:

Plans Huawei Cloud data sync pipelines by classifying workloads, matching suitable services, and preparing Markdown and Excel reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and cloud architects use this skill to assess existing data sync pipelines, choose Huawei Cloud integration services, and document a migration or integration plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Migration advice may suggest disabling authentication or changing encryption settings without explaining the security impact.

Mitigation: Preserve existing authentication where possible, and have the security owner review and approve any authentication or encryption changes before implementation.

## Reference(s):

- [Pipeline classification](references/pipeline-classification.md)
- [Product mapping](references/product-mapping.md)
- [Source-target capability matrix](references/source-target-matrix.md)
- [Solution design algorithm](references/solution-algorithm.md)
- [Instance specifications](references/instance-specs.md)
- [Output verification methods](references/verification-method.md)
- [DataArts Studio offline job data sources](https://support.huaweicloud.com/usermanual-dataartsstudio/dataartsstudio_01_1457.html)
- [CDM data sources](https://support.huaweicloud.com/usermanual-dataartsstudio/dataartsstudio_01_1630.html)
- [DataArts Studio real-time jobs](https://support.huaweicloud.com/usermanual-dataartsstudio/dataartsstudio_01_1601.html)
- [DRS product documentation](https://support.huaweicloud.com/product-drs.html)
- [DLI Flink documentation](https://support.huaweicloud.com/usermanual-dli/dli_01_0438.html)
- [DIS product documentation](https://support.huaweicloud.com/product-dis.html)
- [DMS Kafka documentation](https://support.huaweicloud.com/product-dms.html)
- [OMS product documentation](https://support.huaweicloud.com/product-oms.html)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Excel spreadsheet]

**Output Format:** [Pipeline recommendations in Markdown and a multi-sheet Excel workbook (.xlsx)]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes pipeline classification, product matching, capability checks, solution recommendations, and instance sizing rationale.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
