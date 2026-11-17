## Description:

Generates local images with Ollama's x/z-image-turbo model on macOS and can send the result to WhatsApp.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eric51](https://clawhub.ai/user/eric51)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to generate PNG images from text prompts with a local Ollama model on macOS. The skill can then help share the generated image through WhatsApp with a caption and recipient.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run local Ollama commands and process user prompts through a local image model.

Mitigation: Use explicit user confirmation for generation requests, avoid sensitive prompts, and keep Ollama access limited to the local machine.

Risk: The skill can send generated images and captions to WhatsApp recipients.

Mitigation: Confirm the recipient, caption, and file before sending and avoid sending sensitive or private content.

Risk: The included FastAPI service lacks documented authentication, input limits, and rate limits.

Mitigation: Keep any FastAPI service bound to localhost and add authentication, request limits, rate limits, and safe argument passing before broader use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eric51/skills/ollama-x-z-image-turbo)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration notes, and generated image file paths.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces or references PNG image files generated locally by Ollama and may include WhatsApp message details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
