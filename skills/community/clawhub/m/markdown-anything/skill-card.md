## Description:

Convert PDF, DOCX, XLSX, PPTX, images, audio, and 25+ file formats to clean Markdown using the Markdown Anything API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adiologydev](https://clawhub.ai/user/adiologydev)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to convert user-selected documents, images, and audio files into Markdown for prompts, summaries, and downstream workflows. It also supports checking the Markdown Anything account credit balance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected files are sent to Markdown Anything for processing.

Mitigation: Use the skill only for files that are appropriate to process with the Markdown Anything service and review the linked privacy policy before use.

Risk: The MDA_API_TOKEN is used for API authentication and may be visible to local process observers while curl requests run.

Mitigation: Use a limited-scope or revocable token where possible and avoid running the skill in environments with untrusted local users.

## Reference(s):

- [Markdown Anything](https://markdownanything.com)
- [Markdown Anything workspace](https://markdownanything.com/workspaces)
- [ClawHub skill page](https://clawhub.ai/adiologydev/skills/markdown-anything)
- [Markdown Anything privacy policy](https://markdownanything.com/privacy)

## Skill Output:

**Output Type(s):** [Markdown, Text, Shell commands, Configuration guidance]

**Output Format:** [Markdown to stdout for conversions and plain text for credit-balance checks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MDA_API_TOKEN; optional conversion flags can request enhanced AI, metadata inclusion, or token optimization.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
