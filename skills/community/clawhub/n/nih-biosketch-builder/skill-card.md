## Description:

Generate NIH Biosketch documents compliant with the 2022 OMB-approved format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, administrators, and grant-writing agents use this skill to create NIH-style biosketch DOCX files from structured JSON data and optional PubMed publication imports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The executable skill has under-controlled dependency and file path handling.

Mitigation: Review before installing, run in a sandboxed workspace, pin and verify dependencies, and use only explicit input and output paths that are acceptable to read from or overwrite.

Risk: The packaged requirements list names docx, while the security guidance identifies python-docx as the intended dependency.

Mitigation: Replace docx with python-docx and verify dependencies before execution.

Risk: PubMed import or search can send publication identifiers or author queries to NCBI.

Mitigation: Avoid sensitive grant or biosketch data in shared or synced locations and treat PubMed lookups as external network disclosure.

Risk: Archived audit evidence found one partial stress scenario related to executable path and fallback behavior.

Mitigation: Use validated runnable commands and require a strict fallback response when parameters are missing or execution fails.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/aipoch-ai/skills/nih-biosketch-builder)
- [NIH Biosketch Format Instructions](https://grants.nih.gov/grants/forms/biosketch.htm)
- [SciENcv](https://www.ncbi.nlm.nih.gov/sciencv/)
- [Audit Reference](artifact/references/audit-reference.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [DOCX or JSON files with concise Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit input and output paths; optional PubMed import sends publication identifiers or author queries to NCBI.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
