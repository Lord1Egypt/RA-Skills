## Description:

Converts text to speech using Xiaomi MiMo-V2-TTS with emotional style control, Chinese dialect support, role voices, and singing synthesis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ddpie](https://clawhub.ai/user/ddpie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to synthesize spoken audio from supplied text through Xiaomi MiMo-V2-TTS, including style, emotion, dialect, and singing controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The script can install an unpinned Python dependency at runtime.

Mitigation: Review and install dependencies through a trusted dependency process before use, and run the script in an environment where it cannot auto-install packages.

Risk: Input text and style instructions are sent to the Xiaomi MiMo API, and generated audio is stored locally.

Mitigation: Do not submit confidential, regulated, or secret text unless the user accepts that sharing and storage, and protect or remove generated audio files as appropriate.

Risk: Passing the API key with --api-key can expose credentials through shell history or process listings.

Mitigation: Prefer the MIMO_API_KEY environment variable and manage the key through normal secret-handling practices.

## Reference(s):

- [Xiaomi MiMo Platform](https://platform.xiaomimimo.com)
- [Xiaomi MiMo API Base](https://api.xiaomimimo.com/v1)
- [ClawHub Skill Page](https://clawhub.ai/ddpie/skills/mimo-v2-tts)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell command examples and local audio file output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local audio files in mp3, wav, pcm, opus, or flac format; requires a Xiaomi MiMo API key.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
