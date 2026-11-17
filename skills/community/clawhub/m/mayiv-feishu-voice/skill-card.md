## Description:

Feishu Voice converts text to speech with Edge TTS and sends voice, or paired text and voice, messages to Feishu using environment-provided credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayiv-ai](https://clawhub.ai/user/mayiv-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation agents use this skill to send generated voice messages, or paired text and voice summaries, to Feishu recipients or chats from shell workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provided text and generated audio are sent to Edge TTS and Feishu services.

Mitigation: Use the skill only for content that is acceptable to send to those services, and avoid sensitive or regulated content unless the deployment has been reviewed.

Risk: The server security summary says Feishu app secrets are handled unsafely enough to require review before installation.

Mitigation: Use a Feishu app with minimal permissions, run on a trusted machine, and fix the curl secret handling before production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mayiv-ai/skills/mayiv-feishu-voice)
- [Project address listed by the skill](https://github.com/Mayiv-Ai/feishu-voice)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Text]

**Output Format:** [Markdown with inline bash commands and environment variable examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local edge-tts, ffmpeg, curl, python3, and Feishu app credentials.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
