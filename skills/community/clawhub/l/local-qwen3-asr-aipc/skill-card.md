## Description: <br>
Provides local offline speech-to-text for Windows audio and video files using Qwen3-ASR with Intel OpenVINO, with network required only for first-time setup and model download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[juan-oy](https://clawhub.ai/user/juan-oy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, developers, and Windows users use this skill to transcribe local audio or video files, process folders in batch or watch mode, and optionally archive transcripts as text or JSON. It is intended for local ASR workflows where inference runs offline after first-time setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: First-time setup may install Python or Git, modify PATH or shell integrations, install packages, clone code, and download about 2 GB of model files. <br>
Mitigation: Review setup actions before installation, prefer manual setup when possible, and run only on Windows systems where those changes are acceptable. <br>
Risk: Transcript archives are kept on local disk and may contain sensitive spoken content. <br>
Mitigation: Treat transcript folders as sensitive data, choose archive locations deliberately, and delete or protect transcript files according to the user's retention needs. <br>
Risk: Broad watch folders can process more local files than intended. <br>
Mitigation: Use narrow input folders for watch mode and confirm the target directory before starting continuous transcription. <br>
Risk: The security summary flags broad Windows setup changes and over-trust in auto-discovered local runtime paths. <br>
Mitigation: Run the pre-flight environment check, avoid using untrusted runtime directories, and verify resolved paths before inference. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/juan-oy/local-qwen3-asr-aipc) <br>
- [Qwen3-ASR repository](https://github.com/QwenLM/Qwen3-ASR.git) <br>
- [Qwen3-ASR OpenVINO model files](https://modelscope.cn/models/snake7gun/Qwen3-ASR-0.6B-fp16-ov/files) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON transcription results, optional text or JSON transcript archive files, and setup or runtime command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include transcript text, detected language, source file metadata, recoverable error summaries, and local archive file paths.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata, SKILL.md) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
