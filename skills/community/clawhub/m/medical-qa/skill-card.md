## Description: <br>
医疗健康知识问答技能。用于帮助用户理解症状含义、解读检查报告结果、了解用药常识、提供何时就医的专业建议。当用户询问健康症状、药品说明、检查报告解读、就医建议等问题时触发此技能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yishuihan132](https://clawhub.ai/user/yishuihan132) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill for general medical and health questions, including symptom meaning, lab report interpretation, medication knowledge, and guidance on when to seek care. It should support understanding and triage, not diagnosis, prescriptions, emergencies, or treatment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Users may include unnecessary personal health identifiers in medical questions sent to the external service. <br>
Mitigation: Ask only for the minimum information needed and avoid names, ID numbers, contact details, full records, or other unnecessary identifiers. <br>
Risk: Users may treat general medical answers as diagnosis, prescription guidance, emergency guidance, or a treatment decision. <br>
Mitigation: Present answers as general information and direct users to qualified medical care for diagnosis, prescriptions, severe symptoms, emergencies, or treatment decisions. <br>


## Reference(s): <br>
- [medical-qa on ClawHub](https://clawhub.ai/yishuihan132/medical-qa) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [String] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a medical knowledge-base answer string, or null when the external service does not return a successful answer.] <br>

## Skill Version(s): <br>
1.0.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
