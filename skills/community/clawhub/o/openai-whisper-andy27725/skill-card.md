## Description: <br>
Local speech-to-text with the Whisper CLI (no API key). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy27725](https://clawhub.ai/user/andy27725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and other users use this skill to run local speech-to-text transcription or translation workflows with the Whisper CLI, including quick command examples and setup notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing OpenAI Whisper through Homebrew may add local dependencies and change the execution environment. <br>
Mitigation: Review the Homebrew formula and dependencies, and install only in an approved local environment. <br>
Risk: Audio files may contain sensitive content, and Whisper model files are cached locally. <br>
Mitigation: Transcribe only approved audio on trusted machines and manage local storage, including the Whisper cache. <br>


## Reference(s): <br>
- [OpenAI Whisper](https://openai.com/research/whisper) <br>
- [ClawHub skill page](https://clawhub.ai/andy27725/openai-whisper-andy27725) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the local whisper command; model files may be downloaded and cached locally on first use.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
