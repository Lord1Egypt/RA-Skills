## Description:

Generate new images and edit existing images with xAI Grok Imagine from a local OpenClaw workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stanestane](https://clawhub.ai/user/stanestane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when they want Grok/xAI as the image source for prompt-based image generation, batch variations, reference-image edits, style transfer, cleanup, background replacement, product art, poster concepts, or local automation around xAI image APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The edit command can upload any readable local file path supplied to it, which may expose unintended local content to xAI.

Mitigation: Use only explicitly selected image files from trusted locations, avoid paths that may contain secrets, and add image validation, file-size limits, path restrictions, and upload disclosure before broader deployment.

## Reference(s):

- [xAI Grok Imagine reference](references/api-reference.md)
- [Prompt Templates](references/prompt-templates.md)
- [xAI API Base URL](https://api.x.ai/v1)
- [ClawHub Skill Page](https://clawhub.ai/stanestane/skills/grok-image-generation)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with command examples; script output as JSON plus downloaded image files and response metadata]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XAI_API_KEY and can generate or edit one to ten outputs depending on the selected xAI image endpoint options.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
