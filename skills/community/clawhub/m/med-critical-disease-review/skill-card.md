## Description: <br>
Assesses structured inpatient medical records against 28 critical-disease insurance claim categories by calling a remote assessment service and producing raw JSON plus a natural-language conclusion with evidence. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[unisound-llm](https://clawhub.ai/user/unisound-llm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Claims reviewers and insurance operations teams use this skill to prepare evidence-backed critical-disease claim assessments from inpatient medical records. Developers can run the bundled scripts to normalize common record formats before submitting a supported disease review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical-record contents may be sent to a remote assessment service, and the security evidence says the skill's privacy promises do not match the code behavior. <br>
Mitigation: Use only records you are authorized to process, confirm the remote service's privacy and retention terms, and de-identify sensitive information before running the skill. <br>
Risk: The scripts can write raw assessment JSON, text summaries, and optional prepared medical-record payloads to local output paths. <br>
Mitigation: Choose controlled output locations, restrict access to generated files, and delete outputs that are no longer needed. <br>
Risk: The assessment output supports insurance claim review and could be mistaken for clinical advice. <br>
Mitigation: Use the output as claim-evidence assistance only; route medical diagnosis or treatment questions to qualified clinicians. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/unisound-llm/med-critical-disease-review) <br>
- [Critical-disease assessment API endpoint](https://shangbao.yunzhisheng.cn/skills/critical-disease/api/v1/assessment/assess/{disease}) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Text, JSON, Files] <br>
**Output Format:** [Raw JSON response and natural-language text summary, written to files or printed as a preview.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a supported disease code and medical-record input; optional preprocessing supports JSON, PDF, Office documents, spreadsheets, CSV, text, and image inputs.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
