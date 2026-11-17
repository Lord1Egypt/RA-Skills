## Description:

Local 24x7 OpenAI-compatible API server for STT/TTS, powered by MLX on your Mac.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoqiao](https://clawhub.ai/user/guoqiao)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill on macOS Apple Silicon systems to install and run a local OpenAI-compatible audio API server, then call helper scripts for speech-to-text transcription and text-to-speech audio generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation flow uses a third-party Homebrew tap whose formula can change after review.

Mitigation: Inspect the Homebrew formula before installation and review updates before reinstalling or upgrading.

Risk: The setup can start a persistent background audio API service on the Mac.

Mitigation: Prefer localhost-only use, know how to stop or uninstall the service, and avoid exposing the port beyond trusted local workflows.

Risk: Audio or text submitted for STT/TTS may contain sensitive content.

Mitigation: Avoid sending sensitive audio or text unless you trust the local server and the installed dependencies.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guoqiao/skills/mlx-audio-server)
- [Skill homepage](https://github.com/guoqiao/skills/blob/main/mlx-audio-server/mlx-audio-server/SKILL.md)
- [mlx-audio](https://github.com/Blaizzy/mlx-audio)
- [mlx-audio-server Homebrew formula](https://github.com/guoqiao/homebrew-tap/blob/main/Formula/mlx-audio-server.rb)
- [mlx-audio text-to-speech documentation](https://github.com/Blaizzy/mlx-audio?tab=readme-ov-file#text-to-speech-tts)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash commands; STT output is transcript text and TTS output is an audio file path.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS on Apple Silicon with Homebrew and a localhost OpenAI-compatible API service.]

## Skill Version(s):

0.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
