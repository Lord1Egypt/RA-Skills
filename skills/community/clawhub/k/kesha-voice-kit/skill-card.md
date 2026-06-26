## Description: <br>
Local multilingual voice toolkit for speech-to-text, text-to-speech, and language detection that runs offline on Apple Silicon, Linux, and Windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[drakulavich](https://clawhub.ai/user/drakulavich) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to transcribe voice notes, synthesize voice replies, detect language, and route local audio workflows through a CLI or OpenClaw configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Voice notes may contain sensitive speech, and the documented OpenClaw setup can echo recognized speech into chat history and agent context. <br>
Mitigation: Review OpenClaw transcript echo settings before use and disable or change transcript echoing when handling sensitive audio. <br>
Risk: Installation uses a global Bun package and downloads local engine and model assets. <br>
Mitigation: Install only in environments where global Bun packages and model downloads are approved, and verify the installed `kesha` binary before routing agent audio through it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/drakulavich/kesha-voice-kit) <br>
- [Source repository](https://github.com/drakulavich/kesha-voice-kit) <br>
- [npm package](https://www.npmjs.com/package/@drakulavich/kesha-voice-kit) <br>
- [Release notes](https://github.com/drakulavich/kesha-voice-kit/releases) <br>
- [OpenClaw](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide agents to produce transcripts, timestamped JSON, OGG/Opus voice-note files, WAV audio, and OpenClaw routing configuration.] <br>

## Skill Version(s): <br>
1.5.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
