## Description:

Converts Markdown analysis reports into presentation-ready PPTX files by offering color schemes, planning up to 20 slides, generating nano-banana image prompts and images, assembling the deck, and routing delivery through Feishu or email based on file size.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yunni123](https://clawhub.ai/user/yunni123)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to turn Markdown reports into concise visual PPT presentations with generated slide images and progress updates. It is suited for report-to-deck workflows that need user-selected styling, PPTX assembly, and size-aware delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown report contents may be sent to configured image-generation, Feishu, and email integrations during deck creation and delivery.

Mitigation: Confirm the user accepts those integrations before processing sensitive reports, and avoid highly sensitive inputs when that sharing is not acceptable.

Risk: Large PPTX outputs require email delivery and a recipient address.

Mitigation: Check the actual PPTX file size first, request an explicit recipient address only when the file is over 30 MB, and do not guess or reuse unclear addresses.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yunni123/skills/md-to-nanobanana-ppt)

## Skill Output:

**Output Type(s):** [text, markdown, files, shell commands, guidance]

**Output Format:** [Markdown outline and prompts plus generated PNG images and a PPTX file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Limits presentations to 20 slides; writes outputs under ~/.openclaw/media/ai-choise/md-to-nanobanana-ppt/ and routes PPTX delivery at a 30 MB threshold.]

## Skill Version(s):

1.0.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
