## Description:

Reads meeting notes, summarizes them with the current conversation model, saves local meeting context for follow-up questions, and generates mp3 audio for summaries and answers through SenseAudio TTS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaocaijic](https://clawhub.ai/user/xiaocaijic)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external users can use this skill to turn one meeting note into a short spoken summary, retain local context for follow-up questions, and create mp3 answers for later review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive meeting contents may be retained as plaintext local JSON, and the release includes populated memory files.

Mitigation: Use only meeting notes approved for local retention, remove bundled memory JSON files before installation or release, and provide a clear deletion path for saved meeting context.

Risk: Meeting text, summaries, or answers may be sent to SenseAudio for speech generation.

Mitigation: Get explicit user consent before TTS generation, avoid sensitive or internal URLs, and prefer sending summaries or answers instead of full meeting text.

Risk: The scanner verdict is suspicious because the skill handles meeting notes broadly, even though no clear malicious behavior was reported.

Mitigation: Review the skill before installing, confirm the expected data flow, and keep generated audio and memory files in approved local paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiaocaijic/skills/meeting-minutes-qa-tts)
- [SenseAudio API key docs](https://senseaudio.cn/docs/api-key)
- [Product brief](artifact/PRD.md)

## Skill Output:

**Output Type(s):** [Text, Files, JSON, Shell commands, Guidance]

**Output Format:** [Text responses, local JSON memory files, and mp3 audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SENSEAUDIO_API_KEY when available, asks for mp3 output paths before audio generation, and stores meeting context locally by default.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
