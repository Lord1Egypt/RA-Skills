## Description:

Generates structured outpatient initial-visit medical record text from Chinese doctor-patient dialogue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare users can use this skill to convert Chinese doctor-patient dialogue, including ASR transcripts or normalized document inputs, into a draft initial outpatient medical record for physician review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends full medical dialogue and diag_id values to an external service, and server security evidence says the implementation does not perform the de-identification promised in its documentation.

Mitigation: Use only when authorized to send the data to the external service, remove patient-identifying information before input, and require clinician review of the generated record.

Risk: The optional --save-prepared mode can retain normalized medical dialogue as a plaintext intermediate file on disk.

Mitigation: Avoid --save-prepared for sensitive cases unless retention is intentional and the output location is protected and cleaned up.

Risk: Document and OCR preprocessing can parse untrusted PDF, office, spreadsheet, and image files with optional external tools.

Mitigation: Run preprocessing for untrusted files in an isolated environment with only the required optional dependencies installed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/med-initial-record-genenration)
- [Backend record generation API](https://shangbao.yunzhisheng.cn/skills/record-gen/gen_record_by_diag_v1)

## Skill Output:

**Output Type(s):** [text]

**Output Format:** [UTF-8 plain text with structured outpatient medical-record sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write the generated record to a user-specified output path.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
