## Description:

Edit and enhance images and videos with AI via muapi.ai, including prompt-based editing, upscaling, background removal, face swap, lipsync, and video effects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anil-matcha](https://clawhub.ai/user/anil-matcha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run MuAPI media workflows for prompt-based image editing, image enhancement, lipsync, and video effects on user-supplied images, audio, and video.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Helper scripts execute a local .env file, so running them from an untrusted directory can execute unexpected shell content.

Mitigation: Audit the scripts and working directory before use, and run the skill only from trusted project directories.

Risk: The --add-key flow stores MUAPI_KEY in plaintext in the current directory.

Mitigation: Prefer exporting MUAPI_KEY in the shell or another managed secret store, and avoid using --add-key.

Risk: Local image, audio, and video file arguments may be uploaded to muapi.ai for processing.

Mitigation: Use only media that is approved for third-party processing and review privacy requirements before uploading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anil-matcha/skills/muapi-edit)
- [MuAPI API endpoint](https://api.muapi.ai/api/v1)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and JSON-capable command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands can upload local media files to muapi.ai and return asynchronous request IDs or generated media URLs.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
