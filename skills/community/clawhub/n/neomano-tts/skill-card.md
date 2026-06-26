## Description: <br>
Text-to-speech (TTS) via ElevenLabs for generating spoken audio or voice-note responses from user-provided text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[elandivar](https://clawhub.ai/user/elandivar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to turn supplied text into an MP3 voice note through ElevenLabs, selecting a voice ID when no default voice is configured. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided text is sent to ElevenLabs with an API key, which may expose sensitive content to an external provider. <br>
Mitigation: Use the skill only for text that is acceptable to process with ElevenLabs, keep ELEVENLABS_API_KEY in the runtime environment, and avoid highly sensitive text unless that provider handling is acceptable. <br>
Risk: Audio generation fails when ELEVENLABS_API_KEY or a voice ID is missing or misconfigured. <br>
Mitigation: Configure ELEVENLABS_API_KEY and either ELEVENLABS_VOICE_ID or --voice-id before use, then confirm the generated output file path. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/elandivar/neomano-tts) <br>
- [ElevenLabs text-to-speech API endpoint](https://api.elevenlabs.io/v1/text-to-speech/{voice_id}) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with a shell command and an audio file path; the helper writes MP3 audio by default.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3, ELEVENLABS_API_KEY, and a voice ID from ELEVENLABS_VOICE_ID or --voice-id; default model is eleven_multilingual_v2.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
