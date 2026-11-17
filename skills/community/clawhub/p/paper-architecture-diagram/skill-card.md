## Description:

Automates analysis of local medical image segmentation papers through Gemini and saves extracted architecture-diagram prompts to a local text file.

This skill is ready for commercial/non-commercial use.

## Publisher:

[m1ss-cell](https://clawhub.ai/user/m1ss-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to process medical image segmentation PDFs, extract model-architecture analysis, and produce diagram-generation prompts for paper explanation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The selected local PDF is uploaded to Gemini.

Mitigation: Use the skill only with documents approved for upload to Gemini and avoid sensitive or restricted PDFs unless that transfer is permitted.

Risk: The output file may overwrite an existing analysis text file with the same paper name.

Mitigation: Check for an existing output file before running or keep backups of prior analysis files.

Risk: Weak paper_name validation may allow unsafe path values.

Mitigation: Use only trusted basename values without slashes, path traversal segments, or unexpected suffixes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/m1ss-cell/skills/paper-architecture-diagram)
- [Publisher profile](https://clawhub.ai/user/m1ss-cell)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, shell commands]

**Output Format:** [Markdown-like text with named diagram prompts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes extracted prompt text to a local analysis file using the provided paper name.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
