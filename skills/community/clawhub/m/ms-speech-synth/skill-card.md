## Description: <br>
将长文本（最多数千字）使用微软 Edge TTS 分段合成 MP3/WAV 音频。支持单文件和文件夹批量模式，自动降速防限流（可配置 20-30次/分钟），自动清洗 Markdown 格式转为自然朗读，并可选添加背景音乐（片头/片尾纯背景音）。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[booynal](https://clawhub.ai/user/booynal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and developers use this skill to convert long Chinese text or Markdown files into synthesized MP3/WAV speech, with optional folder batching and background music mixing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected text is sent to Microsoft/Edge TTS for synthesis. <br>
Mitigation: Do not process confidential or regulated documents unless external text-to-speech processing is approved. <br>
Risk: Batch mode can process every supported text or Markdown file in a folder. <br>
Mitigation: Review folder contents before running batch synthesis to avoid sending unintended files. <br>
Risk: Background music mixing depends on a local FFmpeg installation. <br>
Mitigation: Install FFmpeg from a trusted, verified source before enabling background music. <br>
Risk: The Edge TTS interface is rate-limited and does not provide a formal service guarantee. <br>
Mitigation: Use conservative rate and delay settings, and expect retries or pauses for large jobs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/booynal/ms-speech-synth) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Guidance] <br>
**Output Format:** [MP3/WAV audio files with command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes .txt and .md inputs, supports batch folders, configurable voice, chunk size, rate delay, speed, and optional background music settings.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
