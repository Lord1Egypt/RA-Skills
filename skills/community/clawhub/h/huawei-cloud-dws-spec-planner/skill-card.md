## Description:

Plans Huawei Cloud DWS cluster sizing for coupled or decoupled architectures and produces a minimum-spec recommendation with a five-sheet Excel report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huaweicloudskill](https://clawhub.ai/user/huaweicloudskill)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and cloud architects use this skill to size Huawei Cloud DWS clusters for new deployments, migrations, capacity planning, and scale-out decisions.

### Deployment Geography for Use:

Global, subject to DWS flavor availability in the selected Huawei Cloud region.

## Known Risks and Mitigations:

Risk: An optional CLI guide requests OBS credentials and operational access that the core sizing planner does not need.

Mitigation: Review the guide before installation; do not provide cloud credentials or run CLI setup unless OBS access is intentional, and then use temporary least-privilege credentials.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/huaweicloudskill/skills/huawei-cloud-dws-spec-planner)
- [CPU sizing algorithm](references/cpu-sizing-algorithm.md)
- [DWS flavor catalog](references/ecs-flavor-catalog.md)
- [Storage calculation](references/storage-calculation.md)
- [Excel report template](references/excel-report-template.md)

## Skill Output:

**Output Type(s):** [Markdown, Excel spreadsheet, Sizing guidance]

**Output Format:** [Structured Markdown plan and five-sheet XLSX report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One minimum-spec plan; optional growth and scale-out recommendations when daily incremental data and retention are provided.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; skill frontmatter says 2.5.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
