## Description: <br>
Local speech-to-text with the faster-whisper backend (CTranslate2). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[magejosh](https://clawhub.ai/user/magejosh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up local faster-whisper transcription on Windows, cache a CTranslate2 model folder, and replace whisper-cli workflows with a faster local engine. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Python package installation can modify the active environment. <br>
Mitigation: Use a virtual environment before installing faster-whisper, ctranslate2, and huggingface_hub. <br>
Risk: Model downloads can consume local disk space and fail if paths are copied without adjustment. <br>
Mitigation: Adapt the Windows cache path to the target machine and reuse a stable local model folder. <br>
Risk: Audio transcription can process sensitive or unauthorized recordings. <br>
Mitigation: Only transcribe audio the user is allowed to process and handle outputs according to applicable privacy requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/magejosh/mj-windows-faster-whisper) <br>
- [SYSTRAN faster-whisper project](https://github.com/SYSTRAN/faster-whisper) <br>
- [Systran faster-whisper-small model](https://huggingface.co/Systran/faster-whisper-small) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline commands and Python snippets; transcription results are plain text unless timestamps or captions are requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local model folders and prefers CPU int8 inference unless GPU support is explicitly configured.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
