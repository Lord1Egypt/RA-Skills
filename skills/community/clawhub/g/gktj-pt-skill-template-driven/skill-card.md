## Description:

Use when generating patient-facing questionnaire analysis reports from uploaded survey spreadsheets or questionnaire tables, especially when the output must include fixed sections, consistent charts, controlled Word typography, and restrained patient-facing wording.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lee-luogen](https://clawhub.ai/user/lee-luogen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to generate patient-facing Chinese questionnaire analysis reports from uploaded survey spreadsheets or copied questionnaire tables. It helps structure the report, create chart-backed section content, and produce Markdown and Word document artifacts while avoiding unsupported clinical claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive patient survey data may be used as input.

Mitigation: Use the skill only in a workspace and retention setting appropriate for patient survey data, and confirm that Chinese patient-facing reports are the intended output.

Risk: The package appears incomplete because referenced scripts and rule files are not included in the artifact.

Mitigation: Confirm the required local scripts, templates, and rule files are available or provide approved substitutes before relying on generated reports.

Risk: Patient feedback could be overstated as clinical efficacy, safety proof, or medical recommendation.

Mitigation: Keep the report in the patient viewpoint, omit unsupported facts, and avoid absolute efficacy or safety claims.

## Reference(s):

- [Server-resolved source repository](https://github.com/LEE-luogen/GKTJ-Pt-skill-template-driven)
- [ClawHub skill page](https://clawhub.ai/lee-luogen/skills/gktj-pt-skill-template-driven)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated report files, including Markdown, DOCX, chart images, JSON payloads, and summary JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are expected to include report paths, completeness checks, chart count and style checks, missing or uncertain data, and unresolved issues.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
