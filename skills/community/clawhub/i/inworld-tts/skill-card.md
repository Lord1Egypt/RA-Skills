## Description: <br>
Generates text-to-speech audio from text with the Inworld.ai API, supporting multiple voices, speaking rates, MP3 output, and streaming for long text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gugic](https://clawhub.ai/user/Gugic) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to generate MP3 speech audio from text with Inworld.ai voices, speaking-rate controls, temperature settings, and optional streaming for long text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text selected for synthesis is sent to Inworld.ai using the user's API key. <br>
Mitigation: Do not use secrets, private customer data, or regulated content unless the user's Inworld account, permissions, and policies allow it. <br>
Risk: The skill depends on an Inworld API key and local command-line utilities to create audio files. <br>
Mitigation: Store the API key carefully, use the narrowest available permission, and confirm curl, jq, and base64 are available before relying on the workflow. <br>
Risk: The optional global symlink makes the TTS command available from anywhere on the system. <br>
Mitigation: Skip the global symlink unless broad command-line access is needed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Gugic/inworld-tts) <br>
- [Inworld Platform](https://platform.inworld.ai) <br>
- [Inworld API Examples](https://github.com/inworld-ai/inworld-api-examples) <br>
- [Inworld TTS voice endpoint](https://api.inworld.ai/tts/v1/voice) <br>
- [Inworld TTS streaming endpoint](https://api.inworld.ai/tts/v1/voice:stream) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and shell command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces or helps produce MP3 audio files through the bundled shell script.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
