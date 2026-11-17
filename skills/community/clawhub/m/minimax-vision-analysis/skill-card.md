## Description:

Analyze, describe, and extract information from images using the MiniMax vision MCP tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daidai8910g](https://clawhub.ai/user/daidai8910g)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to analyze images, screenshots, charts, UI mockups, and documents through the MiniMax vision MCP tool. It supports description, OCR, UI review, chart extraction, and object detection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected images, including visible text in screenshots or documents, may be sent to MiniMax for processing.

Mitigation: Avoid confidential images unless policy allows it, and restrict MCP file access where possible.

Risk: The skill relies on an unpinned MCP server package and API credentials.

Mitigation: Use a limited MiniMax API key and prefer a pinned, reviewed MCP package version.

## Reference(s):

- [MiniMax Vision Analysis ClawHub release page](https://clawhub.ai/daidai8910g/skills/minimax-vision-analysis)
- [MiniMax Token Plan MCP guide](https://platform.minimaxi.com/docs/token-plan/mcp-guide)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with structured sections, prose, code blocks, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include mode-specific image descriptions, OCR text, UI critiques, chart summaries, object lists, and MCP setup commands.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata.version 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
