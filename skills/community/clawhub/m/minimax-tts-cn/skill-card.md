## Description: <br>
Calls the MiniMax text-to-speech API to generate speech from text, supporting system voices, cloned voices, and configurable audio output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[whille](https://clawhub.ai/user/whille) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to turn Chinese or multilingual text into local audio files through MiniMax TTS. It is useful for voice generation workflows that need selectable voices, speech speed, output format, and voice-list discovery. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided text is sent to MiniMax for speech synthesis. <br>
Mitigation: Do not submit secrets, private messages, regulated data, or confidential drafts unless the MiniMax account terms and data handling are acceptable. <br>


## Reference(s): <br>
- [MiniMax Speech T2A API Documentation](https://platform.minimax.io/docs/api-reference/speech-t2a-http) <br>
- [MiniMax Platform](https://platform.minimax.io) <br>
- [ClawHub Skill Page](https://clawhub.ai/whille/minimax-tts-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration] <br>
**Output Format:** [Audio files with terminal status text and file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MINIMAX_API_KEY and the Python requests package; outputs are saved to a caller-selected local file path or a default tts_output file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
