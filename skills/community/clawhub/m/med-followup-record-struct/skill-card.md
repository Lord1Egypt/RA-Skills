## Description:

Structures Chinese outpatient follow-up medical record text into fine-grained JSON fields such as present illness, past history, diagnosis, and treatment plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[unisound-llm](https://clawhub.ai/user/unisound-llm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to normalize Chinese outpatient follow-up records from text or common document and table formats, then extract structured JSON for downstream record processing. It is a text-structuring aid and does not provide medical diagnosis or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical text may be transmitted to a third-party API during structuring.

Mitigation: Use only records that are approved for transmission to the named third-party service, and assume the full record may be sent unless independently verified redaction is added.

Risk: The documentation promises de-identification, but the security evidence says the code does not implement verifiable redaction.

Mitigation: Redact patient identifiers before invoking the skill, or add and review a redaction step before use with real patient data.

Risk: Document, spreadsheet, PDF, and OCR preprocessing may handle untrusted files.

Mitigation: Run broad file parsing in a sandbox with pinned dependencies and restrict accepted file types where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/unisound-llm/skills/med-followup-record-struct)
- [Backend structuring service endpoint](https://shangbao.yunzhisheng.cn/skills/record-struct/gen_abstract_by_his)

## Skill Output:

**Output Type(s):** [JSON, Files]

**Output Format:** [UTF-8 JSON with Chinese medical record field keys]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a structured JSON file to the requested output path; the unified entrypoint can optionally save normalized prepared text for debugging.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
