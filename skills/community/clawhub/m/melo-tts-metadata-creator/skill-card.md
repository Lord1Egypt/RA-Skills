## Description: <br>
Generates MeloTTS metadata.list files from .wav audio and matching .txt transcripts, with optional Whisper transcription for missing text. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangminrui2022](https://clawhub.ai/user/wangminrui2022) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and voice dataset maintainers use this skill to prepare MeloTTS training or fine-tuning datasets by pairing audio files with transcripts and generating the required metadata.list format. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make broad Python environment changes and download packages or models at runtime. <br>
Mitigation: Run it in an isolated environment and review package installation behavior before use, especially on shared or production systems. <br>
Risk: The skill reads local audio and transcript directories and writes metadata, generated transcripts, logs, and model files. <br>
Mitigation: Use only approved input and output directories, avoid sensitive transcript content, and inspect generated files before using them for training. <br>
Risk: Whisper and ML package downloads can be large and persistent. <br>
Mitigation: Confirm network, disk, and cache expectations before enabling transcription or first-run dependency setup. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangminrui2022/melo-tts-metadata-creator) <br>
- [Artifact README](artifact/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [MeloTTS metadata.list text file plus concise command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each metadata line uses the audio path, speaker, language code, and transcript separated by pipe characters.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
