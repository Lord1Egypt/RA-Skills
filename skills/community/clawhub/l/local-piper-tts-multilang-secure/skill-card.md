## Description:

Local offline text-to-speech via Piper TTS with self-contained setup, automatic language detection, per-call voice selection, and OpenClaw workspace output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[szafranski](https://clawhub.ai/user/szafranski)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to generate local text-to-speech audio files from text, choose or download Piper voices, and manage speech speed without API keys. It is useful when generated speech should remain local after setup while still producing shareable workspace audio files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup installs piper-tts and related dependencies from PyPI into a local virtual environment.

Mitigation: Install only after user confirmation, and review or pin dependencies when stronger supply-chain control is required.

Risk: Voice model acquisition requires optional HTTPS downloads before offline speech generation is available.

Mitigation: Download only selected voices from the documented Piper voice catalog and treat offline operation as applying after setup and model acquisition.

Risk: TTS may fail or degrade if required local dependencies such as ffmpeg, python3, or espeak-ng are unavailable.

Mitigation: Check status before first use and install the documented local prerequisites for the target platform.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/szafranski/skills/local-piper-tts-multilang-secure)
- [Piper Voice Model Catalog](https://github.com/rhasspy/piper/blob/master/VOICES.md)

## Skill Output:

**Output Type(s):** [Files, Text, Configuration]

**Output Format:** [JSON or text responses with generated audio file paths; audio files are OGG/Opus by default or WAV when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are written under the OpenClaw workspace TTS directory; setup and voice downloads may require network access, while speech generation is local after setup.]

## Skill Version(s):

1.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
