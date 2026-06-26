## Description: <br>
医疗设备软件问题报告生成器。根据用户输入的缺陷描述自动生成符合规范的问题报告（包含问题现象、复现步骤、环境信息、严重等级、影响分析等），便于提交给开发和测试团队。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gnllk](https://clawhub.ai/user/gnllk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Testing, quality, support, and development teams use this skill to turn medical-device software defect descriptions into structured issue reports for Jira, ZenTao, email handoff, or quality-management records. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic issue-report trigger phrases may activate the skill while a user is only discussing reports. <br>
Mitigation: Confirm the user wants a formal issue report before generating the final structured report. <br>
Risk: Medical-device and customer defect reports may include patient identifiers or sensitive field data. <br>
Mitigation: Avoid including patient identifiers or sensitive field data unless the user's workflow explicitly permits it. <br>
Risk: Keyword-based severity classification may be incomplete for regulated medical-device workflows. <br>
Mitigation: Treat generated severity as an initial triage value and have responsible quality or safety reviewers confirm it before submission. <br>


## Reference(s): <br>
- [医疗设备软件问题报告模板](references/issue-template.md) <br>
- [严重等级判断指南](references/severity-guidelines.md) <br>
- [ClawHub skill page](https://clawhub.ai/gnllk/issue-report-generator) <br>
- [Publisher profile](https://clawhub.ai/user/gnllk) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Text, Guidance] <br>
**Output Format:** [Markdown issue report with structured fields and checklist guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes severity classification, report metadata placeholders, reproduction steps, impact analysis, attachments, and completion prompts.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
