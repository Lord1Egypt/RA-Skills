## Description:

Edit PDF slides and pages visually from natural-language prompts with the nano-pdf CLI and Google's Gemini 3 Pro Image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ps06756](https://clawhub.ai/user/ps06756)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to modify PDF decks and reports by preparing and running nano-pdf commands for visual edits such as fixing typos, updating charts, changing branding, and adding slides.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PDF page images and, in some workflows, full document text can be sent to Google Gemini.

Mitigation: Use only documents permitted by the user's data policy; avoid confidential, regulated, or customer documents unless that external processing is approved.

Risk: The skill relies on executable dependencies that may be installed or invoked outside the skill package.

Mitigation: Use a reviewed, pinned nano-pdf version in an isolated environment with only the target PDF and GEMINI_API_KEY available.

Risk: Broad trigger language could start an external PDF editing workflow when the user request is ambiguous.

Mitigation: Require explicit user approval before dependency installation, paid API use, or sending document content to an external model.

## Reference(s):

- [Skill homepage](https://github.com/ps06756/nano-banana-pdf-skill)
- [Nano-PDF](https://github.com/gavrielc/Nano-PDF)
- [Google AI Studio API keys](https://aistudio.google.com/api-keys)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in edited PDF files when generated commands are executed.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
