## Description:

Voice-first OpenClaw skill powered by MOSS APIs for spoken replies in a preferred timbre from an existing voice_id or a reference audio clip.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiami2019](https://clawhub.ai/user/xiami2019)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to generate spoken responses with MOSS TTS, either by reusing a stable voice_id or cloning from a provided reference audio source.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference voice clips, local audio paths, and reference URLs may be sent to the external MOSS API.

Mitigation: Use only audio and URLs that are approved for sharing with the provider, and avoid private or sensitive voice samples.

Risk: The skill requires a MOSI_API_KEY for external API requests.

Mitigation: Keep the API key protected and do not print or log raw credentials.

Risk: Generated audio files may remain on local storage after use.

Mitigation: Delete generated audio files when they are no longer needed.

## Reference(s):

- [MOSI Studio](https://studio.mosi.cn)
- [ClawHub skill page](https://clawhub.ai/xiami2019/skills/moss-tts)
- [Publisher profile](https://clawhub.ai/user/xiami2019)

## Skill Output:

**Output Type(s):** [Text, API Calls, Files, Configuration instructions, Guidance]

**Output Format:** [Concise text or Markdown status with generated WAV file path, voice_id, duration, and usage details when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local WAV audio files and uses MOSI_API_KEY for external MOSS API requests.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
