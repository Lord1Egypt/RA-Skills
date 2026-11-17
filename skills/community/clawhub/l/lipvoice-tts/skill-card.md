## Description:

LipVoice voice cloning and text-to-speech synthesis: upload reference audio to create voice models, list existing models, synthesize text to speech, and download generated audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cxhcccvvvsder](https://clawhub.ai/user/cxhcccvvvsder)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to manage LipVoice voice models and generate WAV speech output from text through the LipVoice enterprise API. It supports listing, uploading, deleting, and using voice-clone models when the user has an API key and rights to the source audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Voice cloning can process sensitive biometric audio and create outputs that may impersonate a speaker.

Mitigation: Use only reference audio that you own or have explicit consent to clone, and review generated audio before distribution.

Risk: API keys and sensitive text are sent to an external service, and command-line API keys may be exposed through shell history or process listings.

Mitigation: Prefer the LIPVOICE_API_KEY environment variable, avoid sending sensitive text, and rotate credentials if exposure is suspected.

Risk: Generated-audio downloads may send the API key to arbitrary URLs returned by the service.

Mitigation: Confirm or constrain the download host before use so credentials are sent only to trusted LipVoice endpoints.

Risk: The delete command can remove a remote voice model by ID.

Mitigation: Verify the exact audio model ID before invoking delete.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cxhcccvvvsder/skills/lipvoice-tts)
- [LipVoice API endpoint](https://openapi.lipvoice.cn/api/third)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and local WAV file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or delete remote voice models and may download generated WAV audio files.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
