## Description: <br>
Generates structured outpatient initial medical-record text from Chinese doctor-patient dialogue. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaiccee](https://clawhub.ai/user/aaiccee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinicians, medical documentation teams, and agent operators can use this skill to turn Chinese consultation dialogue into a draft outpatient initial-visit record for licensed physician review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Doctor-patient dialogue may contain protected health information and is sent to an external service. <br>
Mitigation: Use only when external processing is allowed under the applicable medical-data privacy obligations, and confirm the destination service is approved before execution. <br>
Risk: The documentation promises de-identification, but the provided script does not implement local removal of identifiers. <br>
Mitigation: Manually remove names, phone numbers, IDs, addresses, and other identifiers before providing input to the skill. <br>
Risk: Generated records may be incomplete or clinically incorrect. <br>
Mitigation: Require review and approval by a licensed physician before using the output in clinical documentation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aaiccee/med-record-gen) <br>
- [External record-generation service endpoint](https://shangbao.yunzhisheng.cn/skills/record-gen/gen_record_by_diag_v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, files, shell commands, guidance] <br>
**Output Format:** [UTF-8 plain text medical-record draft with structured clinical sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script can write the generated record to a local output path.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
