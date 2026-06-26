## Description: <br>
Parse local video files into transcript and AI analysis. Extract audio, transcribe with faster-whisper, analyze with AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jeremycooper2077](https://clawhub.ai/user/jeremycooper2077) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to process local video files into extracted audio, timestamped transcripts, corrected transcripts, and structured AI analysis reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcript text is sent to a configured remote API during analysis. <br>
Mitigation: Review or redact private, business, regulated, or confidential transcripts before running scripts/analyze.js. <br>
Risk: ffmpeg examples use overwrite flags that can replace existing output files. <br>
Mitigation: Run commands in a dedicated output directory or choose unique output filenames. <br>
Risk: The analysis script requires SU2_API_KEY from the local OpenClaw configuration. <br>
Mitigation: Confirm the configured provider and keep the credential out of transcripts, logs, and shared artifacts. <br>


## Reference(s): <br>
- [Video Analyzer ClawHub release](https://clawhub.ai/jeremycooper2077/jc-video-analyzer) <br>
- [Hugging Face mirror endpoint referenced by the skill](https://hf-mirror.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown guidance with shell command examples plus generated text, Markdown, WAV, and optional image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include audio_16k.wav, transcript.txt, transcript_corrected.md, analysis.md, and optional frame images.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
