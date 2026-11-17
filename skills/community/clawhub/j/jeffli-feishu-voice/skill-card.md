## Description:

Generate Feishu-native voice replies with a playable pause/resume bar by synthesizing text, converting it with ffmpeg to Ogg/Opus, and sending it as a voice message.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeffli2002](https://clawhub.ai/user/jeffli2002)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Feishu workspace users use this skill to provide both visible text and a Feishu-native playable voice message for Chinese voice playback, spoken summaries, or replies that should appear as an in-chat audio player.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Chat text may be synthesized through an external TTS tool and then sent into Feishu, which can expose private or sensitive content.

Mitigation: Avoid using the skill for secrets, private records, or sensitive business content unless the user accepts the TTS and Feishu data flow.

Risk: Broad voice-playback triggers can cause unintended audio-message generation.

Mitigation: Use the skill only when the user explicitly requests Feishu voice playback, spoken summaries, or equivalent voice-message behavior.

Risk: The artifact contains unresolved conflict markers in the skill text.

Mitigation: Review and clean the skill documentation before deployment so agents do not receive contradictory or malformed guidance.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, files, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated JSON/file paths from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an Ogg/Opus voice file path intended for Feishu voice-message sending and keeps a visible text reply aligned with the spoken content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
