## Description:

Adds expressive, companion-style speech presets and optional voice cloning support to text-to-speech workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ksuriuri](https://clawhub.ai/user/ksuriuri)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to create warmer, more expressive voice messages, select emotional presets, and route generated speech through either a cloud Noiz backend or local Kokoro backend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Noiz mode can send speech text and reference audio to a third-party service.

Mitigation: Use the Kokoro backend for private speech, and use Noiz only for explicit audio-generation tasks where third-party transmission is acceptable.

Risk: Reference audio for voice cloning may include voices the user does not have rights or consent to use.

Mitigation: Only provide reference audio when the user has consent and rights to use that voice.

Risk: The skill can save a local Noiz API key for convenience.

Mitigation: Review local credential storage before installation and protect or remove the saved key when it is no longer needed.

Risk: The activation scope is broad for expressive speech requests.

Mitigation: Use the skill only for explicit audio-generation tasks and review generated commands before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ksuriuri/skills/noizai-characteristic-voice)
- [Noiz API keys](https://developers.noiz.ai/api-keys)
- [Noiz text-to-speech API endpoint](https://noiz.ai/v1)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org)
- [ripgrep](https://github.com/BurntSushi/ripgrep)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Audio files, Guidance]

**Output Format:** [Markdown guidance with bash commands that produce WAV or MP3 audio files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl and python3; Noiz mode requires NOIZ_API_KEY and may upload text and reference audio, while Kokoro mode runs locally when installed.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
