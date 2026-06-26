## Description: <br>
Generates structured outpatient initial-visit medical record text from Chinese doctor-patient dialogue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinicians, medical documentation teams, and developers can use this skill to convert Chinese doctor-patient dialogue, including ASR-style transcripts, into structured outpatient initial-visit record sections for physician review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical dialogue may contain patient identifiers and can be sent to an external service. <br>
Mitigation: Run only when policy permits that transfer, remove patient identifiers before execution, and have a qualified clinician review the generated record. <br>
Risk: The artifact describes de-identification, but the security evidence says the code does not enforce it. <br>
Mitigation: Treat de-identification as the operator's responsibility and verify input redaction before invoking the skill. <br>
Risk: Prepared dialogue can be written to disk when --save-prepared is used. <br>
Mitigation: Avoid --save-prepared for sensitive data, or write only to an approved secure location with appropriate retention controls. <br>
Risk: PDF, Office, and image inputs require local parsing or OCR tools. <br>
Mitigation: Prefer trusted TXT or JSON inputs, and process document or image inputs only in a controlled environment. <br>
Risk: The default timeout can wait indefinitely for the external service. <br>
Mitigation: Set a finite --timeout value in automated or production workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/med-initial-record-genenration) <br>
- [Backend record-generation service](https://shangbao.yunzhisheng.cn/skills/record-gen/gen_record_by_diag_v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, files] <br>
**Output Format:** [UTF-8 plain text medical record saved to an output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May also save normalized prepared dialogue when requested with --save-prepared.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
