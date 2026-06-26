## Description: <br>
Generate standardized HR workforce dashboards from Excel files: 5 fixed dashboards covering headcount trends, regional distribution, detailed breakdowns, attrition analysis, and contractor/partner distribution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aico233](https://clawhub.ai/user/aico233) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
HR and people-operations users use this skill to turn active employee, termination, and contingent-worker Excel exports into a standardized workforce dashboard bundle for headcount, attrition, and contractor analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator can delete existing files in the selected output folder. <br>
Mitigation: Run it only in a fresh, empty output directory and avoid pointing --output-dir at a home folder, shared drive, project root, or any folder containing files that must be preserved. <br>
Risk: Uploaded spreadsheets and generated dashboards may contain sensitive HR data. <br>
Mitigation: Handle inputs and outputs as sensitive workforce data, restrict sharing, and review clipboard or email contents before sending. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aico233/hr-workforce-dashboard) <br>
- [Workforce Data Spec](references/data_spec.md) <br>
- [字段映射与输入校验](references/field_mapping.md) <br>
- [安装说明与使用实例](references/install_and_examples.md) <br>
- [版式规范](references/layout_spec.md) <br>
- [指标口径定义](references/metric_definitions.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and generated dashboard files such as HTML, PNG, Excel, PowerPoint, and ZIP bundles] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Primary deliverable is a self-contained dashboard.html; optional bundle outputs include PNG, Excel, PowerPoint, summary markdown, and ZIP.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
