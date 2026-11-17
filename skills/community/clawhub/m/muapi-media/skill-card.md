## Description:

Generate AI images, videos, music, and audio from the terminal via muapi.ai, with scripts for text-to-image, text-to-video, image-to-video, music/audio generation, and file upload.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anil-matcha](https://clawhub.ai/user/anil-matcha)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and media automation users can use this skill to call MuAPI media-generation workflows from an agent or terminal session, including image, video, image-to-video, audio, music, and upload tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scripts source a local .env file before calling MuAPI, so a malicious or untrusted working-directory .env could affect execution.

Mitigation: Run the skill only from a controlled directory and avoid projects or folders that may contain an untrusted .env file.

Risk: The --add-key helper can store the MuAPI API key in .env.

Mitigation: Avoid --add-key; set MUAPI_KEY through the shell environment or a secret manager instead.

Risk: Local files passed to --file, --audio-file, --video-file, or upload.sh are uploaded to MuAPI/CDN.

Mitigation: Only upload files that are approved for external processing and distribution through MuAPI/CDN.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/anil-matcha/skills/muapi-media)
- [Publisher profile](https://clawhub.ai/user/anil-matcha)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, JSON, Files, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON responses from MuAPI scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return request IDs, generated media URLs, uploaded CDN URLs, and local media files when view/download options are used.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
