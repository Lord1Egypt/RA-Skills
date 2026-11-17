## Description:

Document to Markdown converter - convert DOCX, PPTX, Excel files to Markdown. Use when extracting content from Word documents, PowerPoint presentations, or Excel spreadsheets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tanis90](https://clawhub.ai/user/tanis90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agents use this skill to extract Markdown from DOCX, PPTX, XLS, and XLSX files for reading, summarization, analysis, or downstream document workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents or URLs are uploaded to MinerU's cloud API for conversion.

Mitigation: Avoid confidential, regulated, or highly sensitive files unless the user has approval to send them to the service.

Risk: The workflow depends on installing and running the mineru-open-api CLI.

Mitigation: Install from trusted package sources and run the CLI in a least-privilege environment.

Risk: Quick extraction has documented size and page limits and may replace embedded images with placeholders.

Mitigation: Check document size and page count before use, and warn users when image fidelity is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tanis90/skills/pptx-to-markdown)
- [Publisher profile](https://clawhub.ai/user/tanis90)
- [MinerU](https://mineru.net)
- [MinerU CLI](https://mineru.net/ecosystem?tab=cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs Markdown only; embedded images may be replaced with placeholders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
