## Description: <br>
Local speech-to-text using OpenAI Whisper that runs fully offline after the initial model download and supports multiple model sizes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[araa47](https://clawhub.ai/user/araa47) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to transcribe local audio files with Whisper, selecting model size, language, timestamp, JSON, and quiet-mode options as needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The initial Whisper model download and cache can be large, especially for larger model choices. <br>
Mitigation: Choose an appropriate model size before first use and ensure local storage and network access are acceptable for the environment. <br>
Risk: The setup relies on uv/pip dependency installation without a lockfile in the reviewed evidence. <br>
Mitigation: Pin package versions or install in an isolated environment before operational use. <br>
Risk: The documentation names scripts/local-whisper while the reviewed bundle contains scripts/transcribe.py. <br>
Mitigation: Verify the command wrapper or invoke the reviewed script path directly before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/araa47/local-whisper) <br>
- [Publisher profile](https://clawhub.ai/user/araa47) <br>
- [PyTorch CPU package index](https://download.pytorch.org/whl/cpu) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text transcription or JSON with optional timestamp segments; setup guidance uses Markdown with shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires ffmpeg and a local Whisper model cache after the initial model download.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
