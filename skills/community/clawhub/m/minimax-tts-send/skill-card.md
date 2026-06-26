## Description: <br>
Generates speech audio from text with MiniMax TTS, supports system and cloned voices, and can help send generated audio through OpenClaw messaging channels. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seacozz2007](https://clawhub.ai/user/seacozz2007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to convert text into speech audio with MiniMax voices and optionally send the generated media to a selected messaging channel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill embeds a provider API key. <br>
Mitigation: Rotate the exposed credential and replace it with a user-controlled configured credential before use. <br>
Risk: Text entered for speech generation is sent to the external MiniMax service. <br>
Mitigation: Avoid submitting sensitive text unless the provider terms and privacy handling are acceptable for the use case. <br>
Risk: Generated audio can be sent to a messaging channel and recipient. <br>
Mitigation: Confirm the channel, recipient, and media file before sending generated audio. <br>


## Reference(s): <br>
- [MiniMax Speech T2A API documentation](https://platform.minimax.io/docs/api-reference/speech-t2a-http) <br>
- [ClawHub skill page](https://clawhub.ai/seacozz2007/minimax-tts-send) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files, guidance] <br>
**Output Format:** [CLI text output with a generated audio file path; audio file output in MP3 or the selected audio format.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call the external MiniMax service and may send generated audio through configured OpenClaw messaging channels.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
