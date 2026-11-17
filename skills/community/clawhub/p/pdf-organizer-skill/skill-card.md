## Description:

AI tool that categorizes PDFs by topic, extracts metadata, renames files smartly, and organizes them into hierarchical folders automatically.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yxl184](https://clawhub.ai/user/yxl184)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-heavy users use this skill to configure and run an AI-assisted workflow that classifies, renames, and organizes batches of PDF files by topic and metadata.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF excerpts may be sent to the selected AI provider during content analysis.

Mitigation: Use the skill only with provider settings appropriate for the PDF contents, keep the input folder narrow, and avoid regulated or confidential PDFs unless approved.

Risk: API keys and processed PDF contents should be treated as sensitive.

Mitigation: Store API keys outside shared repositories and rotate them if exposed.

Risk: Batch organization can move or rename files in ways the user did not intend.

Mitigation: Run in dry-run mode first and review planned changes before allowing file movement.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yxl184/skills/pdf-organizer-skill)
- [Publisher profile](https://clawhub.ai/user/yxl184)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend dry-run operation before moving or renaming PDF files.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
