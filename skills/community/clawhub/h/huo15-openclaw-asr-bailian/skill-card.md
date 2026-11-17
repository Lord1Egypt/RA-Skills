## Description:

Routes user-approved audio or video transcription through Alibaba Bailian Paraformer/Fun-ASR using a public share URL, then produces verbatim text, summaries, and an OpenClaw ASR delivery block.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

External users, employees, and OpenClaw agents use this skill after the user approves cloud transcription of audio or video through Alibaba Bailian. The skill guides URL sharing, DashScope ASR execution, transcript checking, summary generation, and optional Markdown or Word delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recordings are sent through a public share URL to Alibaba Bailian for cloud transcription.

Mitigation: Confirm user consent before upload and use short-lived share links.

Risk: The workflow requires a DashScope API key.

Mitigation: Keep DASHSCOPE_API_KEY in the environment only and do not write it into skill files, logs, or conversation text.

Risk: Cloud transcription may expose sensitive recording content to an external service.

Mitigation: Review recordings for sensitivity before use and choose a local ASR workflow when cloud processing is not acceptable.

Risk: An unpinned dashscope dependency can change behavior across installs.

Mitigation: Use a pinned dashscope version in an isolated environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zhaobod1/skills/huo15-openclaw-asr-bailian)
- [Publisher homepage](https://cnb.cool/huo15/ai/huo15-skills)
- [Alibaba Cloud Bailian recording file recognition](https://help.aliyun.com/zh/model-studio/recording-file-recognition)
- [Alibaba Cloud Paraformer Python SDK](https://help.aliyun.com/zh/model-studio/paraformer-recorded-speech-recognition-python-sdk)
- [Skill SOP](docs/SOP.md)
- [Transcription script README](scripts/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, plain text transcripts, and structured OpenClaw ASR delivery blocks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include optional Markdown or Word document output after user confirmation.]

## Skill Version(s):

1.0.3 (source: SKILL.md frontmatter, _meta.json, ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
