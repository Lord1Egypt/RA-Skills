## Description:

将中文门诊复诊病历文本结构化为细粒度字段，输出 JSON（如现病史/既往史/诊断/处理意见等）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaiccee](https://clawhub.ai/user/aaiccee)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, healthcare operations teams, and developers use this skill to transform already-written Chinese outpatient follow-up medical-record text into standardized JSON fields for downstream review, workflow integration, or record processing. Its output is extraction and structuring only, not medical diagnosis or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says full medical-record text may be sent to a hard-coded external service while the skill promises de-identification.

Mitigation: Use only already de-identified records unless enforceable redaction, consent, endpoint, and retention controls are confirmed before use.

Risk: The security evidence says the structured result is written to disk unless the output path is controlled.

Mitigation: Set an approved output path, restrict access to generated files, and delete outputs according to the organization’s health-data handling policy.

Risk: The skill handles medical records and its own documentation states the output is not clinical advice.

Mitigation: Require qualified clinical review before using structured fields for care decisions, diagnosis, or treatment planning.

## Reference(s):


## Skill Output:

**Output Type(s):** [JSON, Files, Shell commands, Guidance]

**Output Format:** [UTF-8 JSON file with structured medical-record fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include fields such as history of present illness, past history, diagnosis, and treatment recommendations; missing fields may be marked as not mentioned when supported by the service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
