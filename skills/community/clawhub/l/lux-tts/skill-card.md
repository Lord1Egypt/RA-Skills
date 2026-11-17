## Description:

Lux Tts provides local text-to-speech integration for OpenClaw with voice management, status checks, command-line use, and a simulated fallback implementation compatible with the LuxTTS API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zs15600770520](https://clawhub.ai/user/zs15600770520)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to add local TTS generation, voice file management, installation checks, and troubleshooting guidance to OpenClaw workflows. It is suited for agents that need private local speech output or a local fallback to cloud TTS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation guidance and runtime behavior create and write local files under fixed Windows paths such as D:/lux-tts.

Mitigation: Install and test in a dedicated low-privilege environment, review target paths before execution, and avoid running with administrator privileges unless explicitly required.

Risk: PowerShell ExecutionPolicy Bypass appears in installation troubleshooting guidance.

Mitigation: Prefer batch or manual install steps where possible, and inspect any deploy or download script before using an execution-policy bypass.

Risk: Voice import and output-path interfaces can copy or write files supplied by callers.

Mitigation: Do not expose these interfaces to untrusted callers; restrict allowed paths and validate voice files before import.

Risk: The current implementation can operate as a simulated TTS path rather than guaranteed real LuxTTS synthesis.

Mitigation: Verify generated audio quality and model loading behavior in the target environment before relying on it for production speech output.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zs15600770520/skills/lux-tts)
- [LuxTTS GitHub](https://github.com/ysharma3501/LuxTTS)
- [Hugging Face LuxTTS Model](https://huggingface.co/YatharthS/LuxTTS)
- [OpenClaw Documentation](https://docs.openclaw.ai)
- [Artifact Skill Documentation](artifact/SKILL.md)
- [Installation Guide](artifact/INSTALL_GUIDE.md)

## Skill Output:

**Output Type(s):** [Audio, JSON, Files, Shell commands, Configuration guidance]

**Output Format:** [Python dictionaries with base64-encoded WAV audio, CLI text output, and Markdown installation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audio output is WAV at 48 kHz when generation succeeds; status and error responses are returned as dictionaries.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
