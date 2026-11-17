## Description:

Generate/edit images with Nano Banana Pro (Gemini 3 Pro Image). Use for image create/modify requests incl. edits. Supports text-to-image + image-to-image; 1K/2K/4K; use --input-image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keyserkazi1](https://clawhub.ai/user/keyserkazi1)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative users use this skill to generate new PNG images or edit existing images through Google's Gemini image API from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts and selected input images are sent to Google's Gemini service.

Mitigation: Avoid sensitive prompts or images unless the user accepts the provider's data handling.

Risk: The workflow requires a Gemini API key and may expose credentials if pasted into chat or command history.

Mitigation: Prefer setting GEMINI_API_KEY outside chat and avoid sharing long-lived API keys in prompts or command lines.

Risk: Runtime dependencies are resolved through google-genai and Pillow.

Mitigation: Run with locked dependency versions in a restricted environment when stronger supply-chain control is required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/keyserkazi1/skills/nano-banana-pro1)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline shell commands and saved PNG image paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The invoked script saves PNG files locally and prints the resolved output path.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
