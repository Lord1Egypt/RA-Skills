## Description:

Translates medical records, lab reports, discharge summaries, prescriptions, pathology and radiology reports, and similar documents into structure-preserving, Chinese-first, original-preserving Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[helenalhq](https://clawhub.ai/user/helenalhq)

### License/Terms of Use:

MIT-0

## Use Case:

External users and care-support teams use this skill to translate sensitive medical records into bilingual, doctor-readable artifacts while preserving source structure. It is especially suited for documents where tables, key-value fields, original text, anchors, and low-confidence items must remain traceable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive medical record content may be sent to the configured AI service.

Mitigation: Use the skill only when the user accepts that disclosure, and prefer a local or approved AI service when privacy requirements demand it.

Risk: PDF export can process unsanitized embedded HTML in translation Markdown.

Mitigation: Render only reviewed Markdown in a sandboxed environment that restricts network and local-file access, and keep renderer dependencies updated.

Risk: Errors in dosages, diagnoses, dates, signatures, or low-confidence cells could affect clinical interpretation.

Mitigation: Preserve anchors and low-confidence markings, then require human review of clinically important items against the source document.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/helenalhq/skills/medical-record-translator)
- [Output Contract](references/output-contract.md)
- [Block Model](references/block-model.md)
- [Quality Checklist](references/quality-checklist.md)
- [Medical Terminology Reference](references/terminology.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Constrained Markdown with optional HTML tables and optional PDF export]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves source anchors, one-to-one block mapping, original text, and clinically important low-confidence review notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
