## Description:

Local Audio2SRT helps an agent generate and deploy a local Apple Silicon audio transcription and translation web app using embedded project templates, Python and Node.js dependencies, MLX Whisper, and a Qwen translation model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tsingchou](https://clawhub.ai/user/tsingchou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical users use this skill to create a local Audio2SRT project for transcribing audio to SRT subtitles and translating transcript segments on Apple Silicon Macs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated backend exposes unauthenticated APIs that can process local files.

Mitigation: Run only in an isolated local environment, bind the backend to 127.0.0.1, restrict CORS, and add an auth token before processing sensitive audio.

Risk: Audio transcription and translation can consume significant host CPU, memory, disk, and model download bandwidth.

Mitigation: Limit access to trusted local users, monitor resource usage, and pin dependency and model revisions before regular use.

Risk: Arbitrary file_path transcription can expose local files if the service is reachable by untrusted clients.

Mitigation: Disable arbitrary file paths or constrain them to a controlled upload directory before exposing the backend beyond a private local session.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tsingchou/skills/localaudio2srt)
- [MLX Whisper Large v3 Turbo 4-bit Model](https://www.modelscope.cn/models/mlx-community/whisper-large-v3-turbo-4bit)
- [Qwen2.5 3B Instruct 4-bit Model](https://www.modelscope.cn/models/mlx-community/Qwen2.5-3B-Instruct-4bit)

## Skill Output:

**Output Type(s):** [Code, Files, Shell commands, Configuration]

**Output Format:** [Markdown guidance with generated project files and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a local web app project and startup workflow for macOS on Apple Silicon.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
