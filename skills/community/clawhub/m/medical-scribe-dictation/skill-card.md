## Description:

Convert physician verbal dictation into structured SOAP notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Clinicians, clinical documentation teams, and agent operators use this skill to transform dictated or pre-transcribed encounter notes into structured SOAP documentation with terminology normalization, confidence scoring, and physician-review warnings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive clinical dictation may be sent to external LLM providers if OpenAI or Anthropic processing is enabled.

Mitigation: Use the local rule-based path unless the organization has approved that provider data flow for PHI.

Risk: Generated SOAP notes can contain incomplete or incorrect clinical details.

Mitigation: Treat outputs as drafts and require clinician review of diagnoses, medications, allergies, treatment plans, and validation warnings before use in a medical record.

Risk: Generated notes may be written to shared or insecure output paths.

Mitigation: Save outputs only to approved secure locations and avoid shared directories for patient data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/medical-scribe-dictation)
- [Publisher profile](https://clawhub.ai/user/aipoch-ai)
- [SOAP note templates](references/soap-templates.md)
- [Medical abbreviations](references/medical-abbreviations.json)
- [Example cases](references/example-cases.md)
- [Medical terminology sources](references/terminology-sources.md)
- [SNOMED CT](https://www.snomed.org/)
- [ICD-10-CM](https://www.cdc.gov/nchs/icd/icd-10-cm.htm)
- [LOINC](https://loinc.org/)
- [RxNorm](https://www.nlm.nih.gov/research/umls/rxnorm/)

## Skill Output:

**Output Type(s):** [Markdown, JSON, Text, Files, Guidance]

**Output Format:** [SOAP note in Markdown or JSON, with confidence score and validation warnings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are drafts for clinician review; optional audio input requires Whisper, and optional LLM parsing can use OpenAI or Anthropic when approved.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
