## Description: <br>
Converts audio/video to MP3, transcribes speech to verbatim text and meeting notes, parses .tty terminal recordings to text, then formats structured output for OpenClaw to classify and judge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and knowledge workers use this skill to convert audio, video, or terminal session recordings into readable transcripts, meeting notes, and a structured OpenClaw delivery block for downstream classification and follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local recordings or terminal logs may contain private or sensitive content, especially if a cloud ASR provider is selected. <br>
Mitigation: Prefer local transcription for private content and review any cloud ASR provider before sending audio or logs. <br>
Risk: Hugging Face credentials may be needed for diarization workflows. <br>
Mitigation: Provide Hugging Face credentials through environment variables such as HF_TOKEN rather than command-line arguments. <br>
Risk: MP3 conversion can overwrite existing output files. <br>
Mitigation: Check output paths before conversion and use a distinct filename for each run. <br>
Risk: Low-quality transcription can lead to inaccurate meeting notes or downstream classification. <br>
Mitigation: Run the documented quality check before final notes and retry with a larger Whisper model when errors are significant. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-openclaw-asr) <br>
- [Auxiliary scripts README](scripts/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with transcripts, meeting-note sections, OpenClaw delivery YAML block, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference generated transcript or note files when the user asks to save results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
