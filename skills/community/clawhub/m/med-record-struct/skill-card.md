## Description: <br>
将中文门诊复诊病历文本结构化为细粒度字段，输出 JSON（如现病史/既往史/诊断/处理意见等）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaiccee](https://clawhub.ai/user/aaiccee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to convert Chinese outpatient follow-up medical record text into sectioned JSON fields for record normalization, review, or downstream processing. It is intended for text extraction and structuring, not clinical diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical record text is sent to an external service for structuring. <br>
Mitigation: Use only already de-identified text unless the publisher provides auditable redaction, consent, endpoint, retention, and data-use controls. <br>
Risk: The artifact claims de-identification and no local persistence, but the security evidence still requires review before use with real records. <br>
Mitigation: Review the workflow before installation, test with synthetic records first, and avoid real patient data until privacy and retention controls are verified. <br>
Risk: Structured output may be incomplete or unsuitable for clinical decisions. <br>
Mitigation: Treat output as text extraction only and require qualified clinical review for any diagnosis, treatment, or patient-care decision. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/aaiccee/med-record-struct) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [UTF-8 JSON written to a file, with shell command usage and guidance in Markdown documentation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes a UTF-8 input text file and can include optional diag_id, department, output path, and timeout parameters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
