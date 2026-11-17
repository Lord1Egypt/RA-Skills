## Description:

Monitor YouTube Live and Bilibili Live streams for spoken keywords using browser SpeechRecognition API transcription.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaoxu1232](https://clawhub.ai/user/xiaoxu1232)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to set up live transcription and keyword-monitoring workflows for YouTube Live and Bilibili Live streams.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Browser speech recognition may access microphone audio while a stream plays through speakers, creating privacy exposure around nearby conversations.

Mitigation: Review before installing, run only where audio capture is appropriate, and require explicit consent and data-flow disclosure before use.

Risk: The release claims keyword alerts, but the security guidance says the publisher should implement the advertised keyword alerts or narrow the claims.

Mitigation: Confirm alert behavior before relying on it, or update the skill claims until keyword alert logic is clearly implemented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaoxu1232/skills/live-stream-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JavaScript code references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May involve headed browser automation, microphone access, and console transcript output.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
