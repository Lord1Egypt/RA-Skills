## Description:

Transcribes audio and video locally on Windows using Qwen3-ASR 0.6B with Intel OpenVINO, requiring network access only for first-time setup and model download.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juan-oy](https://clawhub.ai/user/juan-oy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to transcribe local audio or video files on Windows, including single files, batch folders, and watched folders, while keeping inference local after initial setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can create a persistent local ASR environment, install Python packages, clone code, and download about 2 GB of model data.

Mitigation: Run setup manually from a known skill directory, review installers and dependencies, and verify model files before use.

Risk: Runtime discovery scans local drives for *_openvino ASR state and could select an unexpected existing runtime.

Mitigation: Inspect any existing *_openvino/asr/state.json before use and avoid broad auto-discovery when a known runtime directory can be supplied.

Risk: Transcript archiving and video-audio extraction can write files beside the source media or in a configured archive directory.

Mitigation: Use trusted input paths and archive directories, then review generated transcript and extracted-audio files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/juan-oy/skills/local-qwen3-asr-aipc)
- [Qwen3-ASR repository](https://github.com/QwenLM/Qwen3-ASR.git)
- [Qwen3-ASR OpenVINO model files](https://modelscope.cn/models/snake7gun/Qwen3-ASR-0.6B-fp16-ov/files)

## Skill Output:

**Output Type(s):** [text, JSON, files, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with PowerShell commands and JSON or text transcription results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can optionally archive transcripts as .txt and/or .json files; inference depends on a local Windows OpenVINO environment and downloaded model.]

## Skill Version(s):

1.0.3 (source: server release metadata and SKILL.md SKILL_VERSION)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
