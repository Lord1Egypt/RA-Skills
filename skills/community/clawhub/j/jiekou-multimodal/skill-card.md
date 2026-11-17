## Description:

Executes Jiekou AI multimodal tasks for text-to-image, image editing, text-to-video, image-to-video, text-to-speech, and speech-to-text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ximasadila](https://clawhub.ai/user/ximasadila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and end users use this skill to send multimodal generation, editing, speech synthesis, and transcription requests to Jiekou AI. It is suited for workflows that need generated media URLs, audio output, transcription text, and progress updates around asynchronous video tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys may be exposed if users paste real keys into chat or create config files without protecting file permissions.

Mitigation: Prefer environment variables or a local config file with restricted permissions, and do not paste real API keys into chat.

Risk: Prompts, media URLs, images, audio, or video content are sent to Jiekou AI for processing.

Mitigation: Review Jiekou AI data handling terms before use and avoid sending sensitive, regulated, or confidential content unless approved.

Risk: The security evidence reports unsafe API-key handling and insufficient explanation of third-party data sharing.

Mitigation: Review the skill before installation and add user-facing disclosure or local policy controls where the deployment requires them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ximasadila/skills/jiekou-multimodal)
- [API Reference](artifact/references/api-reference.md)
- [Examples](artifact/references/examples.md)
- [Test Cases](artifact/references/test-cases.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown responses with API request examples, configuration guidance, progress messages, and generated media or transcription results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return URLs for generated images, videos, or audio; video generation uses asynchronous task polling.]

## Skill Version(s):

0.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
