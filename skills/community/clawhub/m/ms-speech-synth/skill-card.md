## Description:

将长文本（最多数千字）使用微软 Edge TTS 分段合成 MP3/WAV 音频。支持单文件和文件夹批量模式，自动降速防限流（可配置 20-30次/分钟），自动清洗 Markdown 格式转为自然朗读，并可选添加背景音乐（片头/片尾纯背景音）。

This skill is ready for commercial/non-commercial use.

## Publisher:

[booynal](https://clawhub.ai/user/booynal)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to convert long Chinese text, Markdown files, or folders of text files into synthesized speech audio with Microsoft Edge TTS. It can optionally mix background music into generated MP3 output for narrated content workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may run an unverified ffmpeg binary from a predictable shared temporary path.

Mitigation: Use a trusted system ffmpeg or pass an explicit trusted --ffmpeg path, and do not follow the /tmp curl download guidance.

Risk: Input text is sent to Microsoft Edge TTS.

Mitigation: Avoid sending confidential, regulated, or otherwise sensitive text unless the service use is approved.

Risk: The skill creates temporary audio files and performs user-level subprocess execution.

Mitigation: Run it only in an environment where temporary audio artifacts and subprocess execution are acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/booynal/skills/ms-speech-synth)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Code, Guidance]

**Output Format:** [MP3 or WAV audio files with Markdown usage guidance, shell commands, and Python result dictionaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports single-file and folder batch input, Markdown cleanup, configurable voice/rate/chunk settings, and optional background music mixing.]

## Skill Version(s):

2.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
