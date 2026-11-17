## Description:

Analyzes uploaded academic papers in PDF, Word, Excel, PPT, TXT, Markdown, or CSV formats and produces structured academic reading reports with source quotations, critical analysis, and a generated Word document.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xuruitian](https://clawhub.ai/user/xuruitian)

### License/Terms of Use:

MIT-0

## Use Case:

External users, students, researchers, and knowledge workers use this skill to deeply read uploaded academic papers, extract their main claims and evidence, and receive a six-dimension Markdown analysis plus a local DOCX report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads uploaded academic documents and may process sensitive or unpublished paper content.

Mitigation: Use it in a constrained workspace and avoid submitting sensitive unpublished documents unless local handling is acceptable.

Risk: The skill creates intermediate analysis data and writes DOCX reports locally, including to the user's desktop.

Mitigation: Review output filenames and paths before generation, and clean up intermediate files after use.

Risk: The analysis workflow can optionally use external search for paper context.

Mitigation: Do not enable external web search unless sending paper context to search tools is acceptable.

## Reference(s):

- [Academic Prompt Template](references/academic_prompt.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis with optional JSON input data and DOCX report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill may write intermediate analysis JSON under the skill directory and a DOCX report to the user's desktop.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
