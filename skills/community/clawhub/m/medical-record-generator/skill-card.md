## Description: <br>
专业的病历撰写助手，按照三步流程生成规范的入院记录。当用户说"写病历"、"生成病历"、"病历助手"、"入院记录"、"medical record"或"病历生成"时使用此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gshatw](https://clawhub.ai/user/gshatw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and clinical documentation teams can use this skill to draft structured admission records from supplied patient details. It is intended for record drafting only and does not provide diagnostic recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive health data and can save generated records locally. <br>
Mitigation: Use only synthetic or properly authorized patient data, avoid unnecessary identifiers, and save outputs only in approved secure locations with a clear deletion and retention plan. <br>
Risk: Unspecified patient details may be filled with normal or standard clinical defaults. <br>
Mitigation: Treat default-filled findings as drafting placeholders, not verified clinical facts, and require clinician review before operational use. <br>
Risk: Generated admission records may be mistaken for diagnostic advice. <br>
Mitigation: Use the output for documentation drafting only; do not rely on it for diagnosis or treatment decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/gshatw/medical-record-generator) <br>
- [gshatw Publisher Profile](https://clawhub.ai/user/gshatw) <br>
- [Medical Record Generator Example](references/example.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Code, Guidance] <br>
**Output Format:** [Markdown admission-record text with optional local markdown file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses supplied patient details and built-in defaults for unspecified record fields.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
