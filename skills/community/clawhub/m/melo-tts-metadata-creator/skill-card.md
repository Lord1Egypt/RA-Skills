## Description:

Generates MeloTTS metadata.list files from WAV audio folders and matching transcript text, with support for single-speaker, multi-speaker, and optional Whisper transcription workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangminrui2022](https://clawhub.ai/user/wangminrui2022)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and voice dataset maintainers use this skill to prepare MeloTTS training or fine-tuning datasets by pairing .wav files with transcripts, assigning speakers, and generating a MeloTTS metadata.list file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may modify Python environments and install large unpinned dependencies when run.

Mitigation: Review dependencies first, pin acceptable versions, and run the skill in an isolated disposable environment.

Risk: Optional Whisper transcription can process local audio and transcript folders and write generated transcripts and metadata.

Mitigation: Use only approved datasets, avoid sensitive audio unless local processing is acceptable, and review generated transcript files.

Risk: Generated metadata records may be malformed if transcripts contain delimiter characters or mismatched text.

Mitigation: Inspect metadata.list for malformed or injected records before using it for MeloTTS training or fine-tuning.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wangminrui2022/skills/melo-tts-metadata-creator)
- [ClawHub publisher profile](https://clawhub.ai/user/wangminrui2022)

## Skill Output:

**Output Type(s):** [Files, Text, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Pipe-delimited UTF-8 metadata.list text file, with command-line usage guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Rows use audio_path|speaker|language|text; output is documented as UTF-8 without BOM.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
