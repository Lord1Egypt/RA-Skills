## Description: <br>
Converts unstructured Chinese clinical notes into structured JSON aligned with HL7 FHIR R4 and Chinese electronic medical record standards. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boboy-j](https://clawhub.ai/user/boboy-j) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare developers and clinical data teams use this skill to turn Chinese admission notes, progress notes, discharge summaries, outpatient records, and lab text into structured FHIR-style JSON for downstream review and integration. It is for data extraction and normalization, not diagnosis or treatment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medical records may contain sensitive patient data, and generated JSON or Markdown previews may preserve that data. <br>
Mitigation: Process records locally, keep generated files in secured locations, avoid pasting real patient data into shared terminals or logs, and use the skill's PII masking behavior for previews. <br>
Risk: Extraction results can be incomplete, low-confidence, or unsuitable for clinical use if relied on without review. <br>
Mitigation: Review outputs manually, use low-confidence flags and source-span audit trails, and treat the skill as a data structuring tool rather than clinical advice. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/boboy-j/medical-record-structuring) <br>
- [Project homepage](https://github.com/openclaw-skills/medical-record-structuring) <br>
- [HL7 FHIR R4](https://hl7.org/fhir/R4/) <br>
- [LOINC](https://loinc.org) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Markdown, Shell commands, Guidance] <br>
**Output Format:** [FHIR-style JSON with an optional Markdown preview and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are produced locally; generated JSON and previews may contain patient data and should be stored securely.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, release evidence, changelog released 2026-05-26) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
