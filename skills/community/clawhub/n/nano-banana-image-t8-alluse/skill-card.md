## Description:

Nano Banana Image T8 helps agents call a Nano Banana-compatible image service to generate or edit images from prompts and optional input images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[flywhale-666](https://clawhub.ai/user/flywhale-666)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to run text-to-image or image-to-image requests against a configured Nano Banana-compatible service, returning concise status, errors, and generated image file paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can store an API key in a plaintext file under the user's home directory.

Mitigation: Prefer temporary environment-based keys where possible, and delete or rotate the saved key when it is no longer needed.

Risk: Prompts and selected images are sent to the configured Nano Banana-compatible service.

Mitigation: Use the skill only with trusted endpoints and avoid submitting private or sensitive images unless that data sharing is acceptable.

Risk: Changing the base URL can route credentials and image data to an untrusted endpoint.

Mitigation: Keep the default service endpoint unless there is a verified operational reason to use another trusted endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/flywhale-666/skills/nano-banana-image-t8-alluse)
- [Publisher profile](https://clawhub.ai/user/flywhale-666)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files, guidance]

**Output Format:** [Plain text or Markdown with command invocations, status messages, error details, and generated PNG file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a user-provided API key and may save generated images under the user's WhaleClaw workspace.]

## Skill Version(s):

0.1.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
