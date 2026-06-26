## Description: <br>
Generates advertising creative with Hologres AI Functions and guides virtual campaign delivery, real-time ROI analysis, and budget recommendations through a SQL-based workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wenbingyu](https://clawhub.ai/user/wenbingyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and marketing operations teams use this skill to create ad images and videos from OSS-hosted materials, simulate channel delivery, analyze ROI in Hologres, and generate campaign strategy recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can create cloud database objects, Dynamic Tables, generated media, and OSS-stored campaign artifacts. <br>
Mitigation: Use a dedicated database or schema and OSS prefix, review SQL before write operations, and clean up generated tables, logs, Dynamic Tables, and OSS media when finished. <br>
Risk: The workflow depends on OSS access and RAM role permissions for source materials and generated media. <br>
Mitigation: Grant a least-privilege RAM role scoped to the required bucket or prefix before running the workflow. <br>
Risk: Generated video URLs can include signed OSS parameters and campaign assets may be sensitive before release. <br>
Mitigation: Avoid sharing signed URLs or unreleased campaign assets outside the intended audience. <br>


## Reference(s): <br>
- [SQL Templates](references/sql-templates.md) <br>
- [Style Templates](references/style-templates.md) <br>
- [Virtual Delivery and ROI Analysis](references/virtual-delivery.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/wenbingyu/hologres-ad-campaign) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with SQL and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes generated SQL templates, execution sequencing, Hologres CLI setup commands, and operational guidance for OSS-backed media generation.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
