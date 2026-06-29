## Description: <br>
MiniMax TTS helps agents generate speech audio from text through the MiniMax HTTP REST API with multilingual voices, streaming or non-streaming requests, and mp3, wav, or pcm output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fuzzyb33s](https://clawhub.ai/user/fuzzyb33s) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and content creators use this skill to convert text into narrated audio, voiceovers, or multilingual speech assets with MiniMax voices. It is useful when an agent needs to propose or run text-to-speech commands and save generated audio locally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Supplied synthesis text is sent to MiniMax's external API. <br>
Mitigation: Avoid submitting secrets, regulated data, or private content unless the MiniMax account and data-handling terms are acceptable for the use case. <br>
Risk: Overriding the API URL can send both text and the bearer token to the chosen endpoint. <br>
Mitigation: Use the documented MiniMax endpoints unless the alternate endpoint is trusted and approved. <br>


## Reference(s): <br>
- [MiniMax TTS Voice Reference](references/voices.md) <br>
- [MiniMax Text-to-Speech API endpoint](https://api.minimax.io/v1/t2a_v2) <br>
- [MiniMax lower-latency Text-to-Speech API endpoint](https://api-uw.minimax.io/v1/t2a_v2) <br>
- [MiniMax Voice Management API documentation](https://platform.minimax.io/docs/api-reference/voice-management-get) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, code, files] <br>
**Output Format:** [Markdown guidance with bash commands and local audio files such as mp3, wav, or pcm] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a MiniMax bearer token, sends supplied text to the configured MiniMax API endpoint, and writes generated audio to the requested local output path.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
