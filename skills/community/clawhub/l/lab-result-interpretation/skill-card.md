## Description:

A medical assistant tool that transforms complex biochemical laboratory test results into clear, patient-friendly explanations with safety disclaimers and severity flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn biochemical lab values into patient-friendly educational explanations with abnormality flags, recommendations, assumptions, and explicit medical disclaimers. It is scoped to lab result explanation and must not be used for diagnosis, treatment, prescribing, or interpretation of imaging, pathology, or genetic tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be used for real medical decisions even though its critical-value handling needs review and clinical verification.

Mitigation: Use it only as educational support, test the loaded critical thresholds before relying on them, and have a qualified healthcare provider interpret concerning results.

Risk: File-based input may expose unintended local report contents if users pass broad or uncontrolled paths.

Mitigation: Run the skill in an isolated workspace and process only files that were explicitly selected for interpretation.

## Reference(s):

- [Standard reference ranges](artifact/references/lab_reference_ranges.json)
- [Patient-friendly explanation templates](artifact/references/explanation_templates.json)
- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/lab-result-interpretation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown responses with structured result objects and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes assumptions, severity flags, critical findings when applicable, safety limits, unresolved items, and a medical disclaimer.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
