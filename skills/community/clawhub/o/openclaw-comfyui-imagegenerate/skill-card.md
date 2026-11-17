## Description:

Generates images through a local ComfyUI service and sends them to a Feishu conversation, returning no text after a successful send.

This skill is ready for commercial/non-commercial use.

## Publisher:

[y93442100-beep](https://clawhub.ai/user/y93442100-beep)

### License/Terms of Use:


## Use Case:

OpenClaw users and developers use this skill to generate an image from a prompt with local ComfyUI and deliver it into the current Feishu chat or user conversation. It fits image-generation workflows where successful delivery should be silent and failures should return clear Chinese feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically sends generated images to the current Feishu conversation.

Mitigation: Install it only where automatic Feishu delivery is expected and the bot has the intended message-send permissions.

Risk: The skill trusts a hard-coded local script path and uploads the file path printed by that script.

Mitigation: Protect the installed skill directory, verify draw.py is the reviewed script, and constrain uploads to generated image files under output_images.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/y93442100-beep/skills/openclaw-comfyui-imagegenerate)
- [Artifact README](artifact/README.md)
- [Artifact skill description](artifact/skill.md)
- [ComfyUI workflow configuration](artifact/zimage-api.json)

## Skill Output:

**Output Type(s):** [text, image files, shell commands, configuration]

**Output Format:** [PNG image files, Feishu image messages, local file paths, silent NO_REPLY on success, and Chinese error text on failure.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local ComfyUI at 127.0.0.1:8188 and Feishu message-send permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
