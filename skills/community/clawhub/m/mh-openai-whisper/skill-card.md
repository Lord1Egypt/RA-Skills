## Description: <br>
Local speech-to-text with the Whisper CLI (no API key). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, analysts, and other users can use this skill to run the local Whisper CLI for speech-to-text transcription or translation of audio files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Audio inputs may contain private or sensitive speech. <br>
Mitigation: Treat audio files and transcripts as sensitive, and only transcribe recordings that are intended to be processed on the local machine. <br>
Risk: The skill depends on a locally installed Homebrew package and downloads Whisper model files on first use. <br>
Mitigation: Confirm the `whisper` CLI is installed from the expected package source and that local model storage is acceptable for the environment. <br>


## Reference(s): <br>
- [OpenAI Whisper research page](https://openai.com/research/whisper) <br>
- [ClawHub skill page](https://clawhub.ai/mohdalhashemi98-hue/mh-openai-whisper) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides local CLI use; transcription output files are produced by the Whisper command selected by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
