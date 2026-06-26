## Description: <br>
Helps an agent classify varied customer planning and demand Excel workbooks into one of three standard templates, normalize their contents, generate filled template workbooks, and mark cell-level differences against prior versions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, operations teams, and developers use this skill to turn inconsistent customer planning spreadsheets into standardized Excel templates and to compare new and old workbook versions for planning changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Customer planning spreadsheets can contain sensitive operational data. <br>
Mitigation: Install and run the skill only in an approved local environment where processing customer spreadsheets is acceptable. <br>
Risk: Unfamiliar, multi-sheet, or irregular workbooks may be misclassified or mapped incorrectly. <br>
Mitigation: Review inspection reports, classification confidence, and generated column mappings before relying on converted templates. <br>
Risk: Unpinned package ranges may resolve to dependency versions that behave differently over time. <br>
Mitigation: Pin dependencies or use a lockfile before production deployment. <br>


## Reference(s): <br>
- [Workflow Guide](artifact/reference/workflow.md) <br>
- [Classification Guide](artifact/reference/classification.md) <br>
- [Template Schema](artifact/reference/templates_schema.json) <br>
- [ClawHub Release Page](https://clawhub.ai/zhaobod1/huo15-openclaw-plan-form) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, code, configuration, files] <br>
**Output Format:** [Markdown guidance with shell commands; generated JSON and Excel files from bundled scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces normalized JSON, standardized Excel templates, annotated Excel diff workbooks, and diff reports when the agent runs the provided scripts.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
