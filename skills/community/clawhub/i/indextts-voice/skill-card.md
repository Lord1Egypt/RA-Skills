## Description:

IndexTTS voice cloning and speech synthesis skill for creating voice models, generating text-to-speech, and managing reference audio; requires an enterprise IndexTTS membership.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cxhcccvvvsder](https://clawhub.ai/user/cxhcccvvvsder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams with IndexTTS enterprise access use this skill to manage voice-clone models, synthesize speech from text, manage short-lived reference audio, and download generated audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The download path may expose the IndexTTS API signing secret to an unvalidated service-returned URL.

Mitigation: Review before installing with real enterprise credentials, keep INDEX_API_SIGN scoped to a secure user environment, and avoid tts-download unless the returned download host is trusted.

Risk: Voice cloning can be misused when source audio is used without rights or consent.

Mitigation: Use only audio samples that the operator has rights and consent to clone or synthesize.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cxhcccvvvsder/skills/indextts-voice)
- [IndexTTS website](https://indextts.cn)
- [IndexTTS developer documentation](https://indextts.cn/main/developer)
- [IndexTTS API base URL](https://openapi.lipvoice.cn/api/third/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, files]

**Output Format:** [Markdown guidance with inline shell commands; the CLI emits JSON responses and can save generated WAV files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires INDEX_API_SIGN; INDEX_BASE_URL defaults to https://openapi.lipvoice.cn.]

## Skill Version(s):

1.3.0 (source: server release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
