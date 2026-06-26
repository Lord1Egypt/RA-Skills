## Description: <br>
Local speech-to-text with the Whisper CLI (no API key). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[czubi1928](https://clawhub.ai/user/czubi1928) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and other users use this skill to generate local Whisper CLI commands for transcribing or translating audio without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing the Homebrew openai-whisper package adds local command-line software and dependencies. <br>
Mitigation: Review the package before installation and install it only in environments where Homebrew-managed dependencies are acceptable. <br>
Risk: Whisper models are downloaded and cached locally on first use. <br>
Mitigation: Confirm the machine has sufficient storage and that local model caching is permitted for the environment. <br>
Risk: Transcripts and output directories may contain sensitive information from source audio. <br>
Mitigation: Treat generated transcript files and output directories as sensitive data when the audio contains private or regulated content. <br>


## Reference(s): <br>
- [OpenAI Whisper](https://openai.com/research/whisper) <br>
- [ClawHub skill page](https://clawhub.ai/czubi1928/openai-whisper-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key is required; Whisper models are downloaded locally as needed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
