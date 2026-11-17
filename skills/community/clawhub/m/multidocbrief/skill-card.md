## Description:

Analyzes a mixed set of documents and produces a structured analytical brief in a Word document of no more than two pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sergeypetrakov](https://clawhub.ai/user/sergeypetrakov)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and other users can use this skill to analyze multiple attached documents and produce a concise brief with an overall conclusion and topic-by-topic summaries and reasoning.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusing an extraction work folder can silently delete existing files in its images and texts subfolders.

Mitigation: Use a fresh, dedicated temporary work directory for each run; select only documents intended for analysis and remove sensitive working copies afterward.

## Reference(s):

- [Multi document brief on ClawHub](https://clawhub.ai/sergeypetrakov/skills/multidocbrief)
- [Example analysis structure](references/example_analysis.json)

## Skill Output:

**Output Type(s):** [Analysis, Files]

**Output Format:** [Microsoft Word DOCX]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A4 document, no more than two pages, with an overall conclusion followed by topic summaries and decision reasoning.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
