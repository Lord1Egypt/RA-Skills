## Description: <br>
ElevenLabs advanced TTS for converting text to speech, listing voices, and managing credits. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrnsmh](https://clawhub.ai/user/mrnsmh) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to call ElevenLabs for text-to-speech generation, voice discovery, and credit checks from a command-line or importable Python workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text is sent to ElevenLabs for text-to-speech generation. <br>
Mitigation: Review text before use and avoid sending confidential or restricted content unless the ElevenLabs account and terms are approved for that data. <br>
Risk: The skill uses an ElevenLabs API key and generated audio can consume account credits. <br>
Mitigation: Prefer the ELEVENLABS_API_KEY environment variable over command-line keys and check credits before large runs. <br>
Risk: Generated audio is written to a user-provided output path. <br>
Mitigation: Review the output path before running to avoid overwriting important files. <br>


## Reference(s): <br>
- [ElevenLabs popular voices and API parameters](references/voices.md) <br>
- [ElevenLabs API v1 endpoint](https://api.elevenlabs.io/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Text, Shell commands] <br>
**Output Format:** [MP3 audio files, JSON voice listings, and plain-text credit summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an ElevenLabs API key and may consume account credits when generating audio.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
