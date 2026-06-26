## Description: <br>
Local Audio2SRT helps an agent generate and deploy a local Audio2SRT web application for Apple Silicon Macs, including embedded React and Python project files, dependency installation steps, ModelScope model downloads, and local backend and frontend startup commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tsingchou](https://clawhub.ai/user/tsingchou) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to create a local MLX Whisper transcription and translation web GUI without cloning source code from a remote repository. It is intended for Apple Silicon macOS environments with Python and Node.js available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated backend is exposed broadly for a local-only transcription tool. <br>
Mitigation: Run only on trusted networks unless the backend is changed to bind to 127.0.0.1 and CORS is restricted. <br>
Risk: The setup installs Python and Node.js dependencies and downloads multi-GB ModelScope models. <br>
Mitigation: Use a fresh dedicated project directory and a virtual environment before installation. <br>
Risk: The generated service can process uploaded files or local file paths. <br>
Mitigation: Limit transcription inputs to uploaded files or an allowlisted directory. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tsingchou/localaudio2srt) <br>
- [Skill instructions](artifact/SKILL.md) <br>
- [File mapping](artifact/references/file-mapping.md) <br>
- [Backend transcription server template](artifact/references/transcribe_server.py) <br>
- [Startup script template](artifact/references/start.sh) <br>
- [Python requirements template](artifact/references/requirements.txt) <br>
- [Node package template](artifact/references/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with generated project files and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a local React and Python Audio2SRT project, installs dependencies, downloads MLX Whisper and Qwen models, and launches local services.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
