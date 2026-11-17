## Description:

Local speech-to-text with the faster-whisper backend (CTranslate2). Use when transcribing audio locally, setting up the faster-whisper model cache, or replacing a whisper-cli workflow with a faster local engine.

This skill is ready for commercial/non-commercial use.

## Publisher:

[magejosh](https://clawhub.ai/user/magejosh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to set up local faster-whisper transcription on Windows, manage a reusable CTranslate2 model cache, and produce plain-text transcriptions from audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Third-party Python packages and model downloads can introduce supply-chain or version drift risk during setup.

Mitigation: Use a dedicated virtual environment or container, install from trusted indexes, pin package versions, and document the model cache location.

Risk: Using whisper.cpp ggml model files with faster-whisper will fail because faster-whisper expects CTranslate2 model folders.

Mitigation: Download and reuse a supported faster-whisper model folder such as Systran/faster-whisper-small instead of ggml binaries.

Risk: GPU-specific settings can cause avoidable local setup failures on machines without compatible GPU configuration.

Mitigation: Default to CPU execution with int8 compute unless the machine is explicitly configured and tested for GPU inference.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/magejosh/skills/mj-windows-faster-whisper)
- [faster-whisper GitHub Repository](https://github.com/SYSTRAN/faster-whisper)
- [Systran faster-whisper-small Model](https://huggingface.co/Systran/faster-whisper-small)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text guidance, with shell commands and Python code when setup or transcription is requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Keeps transcription output plain text unless timestamps or captions are requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
