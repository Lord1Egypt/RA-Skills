## Description: <br>
Transforms rough email drafts into polished, professional medical correspondence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, external medical professionals, and agents use this skill to turn rough mentor, editor, colleague, or patient email drafts into clearer professional correspondence. It supports wording, tone, opening, closing, subject-line, and change-summary suggestions without replacing clinical or compliance review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical or HIPAA-related wording could be mistaken for clinical, legal, or compliance guidance. <br>
Mitigation: Use the skill only to polish wording, avoid unnecessary patient identifiers or confidential details, and have a qualified person review patient-facing or compliance-sensitive emails before sending. <br>
Risk: Drafts may contain sensitive patient or institutional information. <br>
Mitigation: Provide only the minimum necessary detail, remove identifiers when possible, and keep generated outputs in the approved workspace. <br>
Risk: Requests outside the documented email-polishing scope can lead to unsupported assumptions. <br>
Mitigation: Stop when required inputs are missing or the request asks for clinical interpretation, and ask for the minimum additional drafting context needed. <br>


## Reference(s): <br>
- [Medical Email Polisher Guidelines](references/guidelines.md) <br>
- [Medical Email Polisher Audit Result v1](medical-email-polisher_audit_result_v1.json) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/medical-email-polisher) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON object with polished_email, subject_line, changes_made, tone_assessment, and recipient_type fields; narrative agent responses may summarize assumptions, risks, and next checks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are drafting aids and should be reviewed before use in patient-facing or compliance-sensitive contexts.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
