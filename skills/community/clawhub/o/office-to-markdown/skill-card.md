## Description:

Converts explicitly requested PDF, PPTX, DOCX, XLSX, and CSV document conversions into clean Markdown, with optional Claude vision extraction for scanned or image-only content after user confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naimalarain13](https://clawhub.ai/user/naimalarain13)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to convert office documents into readable Markdown files after an explicit conversion request. It is suited to document extraction workflows that need text-first conversion with optional OCR-style vision extraction for image-only pages, slides, or embedded images.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can upload document images to an external Anthropic API when vision extraction is enabled.

Mitigation: Use the text-only conversion path by default, require explicit user confirmation before vision extraction, and avoid the vision option for confidential documents unless external transmission is acceptable.

Risk: The skill automatically installs runtime packages during conversion.

Mitigation: Run the skill in a sandboxed environment and prefer deployment packaging that preinstalls locked dependencies before use.

Risk: Server security evidence marks the release as suspicious because external image upload and runtime dependency installation have weak enforcement boundaries.

Mitigation: Review the skill before installing, scan it before deployment, and limit use to documents and environments where those behaviors are acceptable.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/naimalarain13/skills/office-to-markdown)
- [Anthropic Messages API endpoint used by vision extraction](https://api.anthropic.com/v1/messages)

## Skill Output:

**Output Type(s):** [markdown, shell commands, guidance]

**Output Format:** [Markdown files with brief text summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces one Markdown output file per conversion; vision extraction is optional and should be used only after user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
