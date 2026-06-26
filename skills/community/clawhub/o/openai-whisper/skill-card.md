## Description: <br>
Local speech-to-text with the Whisper CLI (no API key). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to transcribe or translate local audio files with the Whisper CLI without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Homebrew package and local Homebrew setup are part of the installation trust boundary. <br>
Mitigation: Install only from a trusted Homebrew setup and review the package source before deployment. <br>
Risk: Whisper model files are downloaded and cached locally on first use. <br>
Mitigation: Plan storage and network access for model downloads, and manage the local cache according to organizational policy. <br>
Risk: Generated transcripts can contain sensitive information from the input audio. <br>
Mitigation: Handle audio files and transcript outputs as sensitive data and apply the same access controls and retention rules. <br>


## Reference(s): <br>
- [OpenAI Whisper research page](https://openai.com/research/whisper) <br>
- [ClawHub skill page](https://clawhub.ai/steipete/openai-whisper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated Whisper outputs depend on the command flags, such as text or subtitle files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
