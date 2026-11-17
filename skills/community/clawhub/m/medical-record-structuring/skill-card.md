## Description:

Convert unstructured Chinese clinical narratives into structured JSON aligned with HL7 FHIR R4 and Chinese EMR standards for record parsing, entity extraction, and FHIR-oriented output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boboy-j](https://clawhub.ai/user/boboy-j)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, data engineers, and healthcare operations teams can use this skill to structure Chinese admission notes, progress notes, discharge summaries, outpatient records, and lab text into machine-readable clinical data. It is intended for data extraction and normalization workflows, not clinical diagnosis or treatment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review says the skill's privacy and standards-compliance claims are stronger than what the bundled code actually provides.

Mitigation: Treat generated FHIR, WS 445, ICD, and LOINC outputs as lightweight extraction artifacts that require validation by qualified reviewers before production or regulated use.

Risk: The skill can process real patient records, and stdout or generated output files may contain protected health information.

Mitigation: Use only approved local workspaces for real patient data and avoid writing outputs to shared folders, logs, or source control unless PHI controls have been reviewed.

Risk: The bundled extractor is local and rule-based in the artifact, so missed entities, incorrect mappings, and low-confidence fields are possible.

Mitigation: Review extraction reports, warnings, and low-confidence fields before downstream use, and add site-specific dictionaries or validation checks for production workflows.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/boboy-j/skills/medical-record-structuring)
- [Project Homepage](https://github.com/openclaw-skills/medical-record-structuring)
- [HL7 FHIR R4](https://hl7.org/fhir/R4/)
- [LOINC](https://loinc.org)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON extraction payloads, FHIR Bundle JSON, Markdown previews, and command-oriented workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may contain protected health information; previews mask patient identifiers where supported, but generated files and stdout should be handled as sensitive data.]

## Skill Version(s):

1.0.0 (source: frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
