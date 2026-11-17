## Description:

Generate images, music, and video using the Pollinations AI API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kanfred](https://clawhub.ai/user/kanfred)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to generate images, music or audio, and videos from text prompts through Pollinations AI command-line scripts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API-key handling and file-output controls require review before installation.

Mitigation: Use a low-privilege Pollinations API key, keep generated files in a trusted output directory, and review the scripts before running them.

Risk: Prompts and generated media may be sent to external services, including Telegram when enabled.

Mitigation: Avoid private prompts and use --telegram only when the configured chat is intended to receive the generated image and caption.

Risk: Dependencies are not pinned in requirements.txt.

Mitigation: Pin and review dependency versions before deploying the skill in a shared or production environment.

## Reference(s):

- [Pollinations API Documentation](https://gen.pollinations.ai/api/docs)
- [Pollinations Website](https://pollinations.ai/)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions, Files]

**Output Format:** [Markdown guidance with inline shell commands; generated artifacts are image, audio, or video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a POLLINATIONS_API_KEY environment variable; optional Telegram delivery requires TELEGRAM_CHAT_ID.]

## Skill Version(s):

1.0.4 (source: _meta.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
