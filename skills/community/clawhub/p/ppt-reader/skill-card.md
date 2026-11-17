## Description:

Reads PowerPoint PPTX files and extracts slide text content for review, summarization, and basic presentation analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jingqiu2180](https://clawhub.ai/user/jingqiu2180)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill when an agent needs to inspect a PPTX file, count slides, extract per-slide text, and organize the result into a structured summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unknown or very large PPTX files can create resource-use or excessive-output issues when processed with local unzip and text extraction commands.

Mitigation: Use trusted or reasonably sized presentations, and apply file-size, slide-count, timeout, and output limits before processing unknown PPTX files.

Risk: Extracted PPTX text may omit images, charts, formatting, layout, and some complex table content.

Mitigation: Treat extracted text as a partial content view and review the original presentation when visual or formatting details matter.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jingqiu2180/skills/ppt-reader)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and extracted text summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill produces local extraction commands and human-readable slide text; it does not extract images, charts, styling, or legacy .ppt files.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
