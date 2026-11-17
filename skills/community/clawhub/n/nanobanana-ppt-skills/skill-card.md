## Description:

Generates presentation slide images from user-provided documents and can optionally create transition videos, interactive playback pages, and full presentation videos.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itrocker](https://clawhub.ai/user/itrocker)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to turn source documents or pasted text into structured slide plans, generated presentation images, optional transition videos, interactive HTML viewers, and full MP4 presentation videos.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API credentials may be exposed through prompts or local setup examples.

Mitigation: Configure keys locally or through a secret store, do not paste keys into agent prompts, rotate any key copied into chat, and restrict provider key permissions.

Risk: The server security review found environment and installation behavior too broad for automatic approval.

Mitigation: Review before installing, use an isolated environment, pin dependencies, and install only after the package narrows .env loading and ships safe environment templates.

Risk: The skill sends presentation source material to configured third-party generation services.

Mitigation: Use only document content approved for those provider accounts and review generated media before sharing or publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/itrocker/skills/nanobanana-ppt-skills)
- [Google AI Studio API keys](https://aistudio.google.com/apikey)
- [Kling AI platform](https://klingai.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance plus JSON slide plans, shell commands, PNG images, HTML viewers, and optional MP4 videos.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided document content and a Google API key for image generation; optional Kling credentials and FFmpeg enable video outputs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
