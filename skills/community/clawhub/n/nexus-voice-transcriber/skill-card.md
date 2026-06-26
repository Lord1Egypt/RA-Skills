## Description: <br>
Transcribes voice notes and audio or video files with local Whisper or optional Deepgram, then saves transcripts and optional source audio for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[matthew00ita](https://clawhub.ai/user/matthew00ita) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to transcribe voice notes, meetings, interviews, or videos into saved text, subtitle, or JSON outputs. It supports private local Whisper processing and optional Deepgram diarization when the user accepts sending audio to Deepgram. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Transcripts and optional source audio may contain sensitive personal or business information and are saved locally. <br>
Mitigation: Use approved local storage locations, review transcript contents before sharing, and delete retained audio or transcript files according to the user's data policy. <br>
Risk: Choosing Deepgram sends audio to an external transcription provider. <br>
Mitigation: Use local Whisper for private recordings; use Deepgram only when the user intentionally accepts external processing and has configured DEEPGRAM_API_KEY. <br>
Risk: URL input and very large media files can increase exposure to untrusted content, excessive downloads, or processing failures. <br>
Mitigation: Avoid untrusted or very large URLs, prefer local files from known sources, and split long recordings before transcription. <br>


## Reference(s): <br>
- [NEXUS Voice Transcriber on ClawHub](https://clawhub.ai/matthew00ita/nexus-voice-transcriber) <br>
- [Whisper Models Guide](references/whisper-models.md) <br>
- [Troubleshooting Guide](references/troubleshooting.md) <br>
- [Deepgram Documentation](https://developers.deepgram.com/docs) <br>
- [FFmpeg Downloads](https://ffmpeg.org/download.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, subtitle files, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples; generated transcripts as txt, srt, vtt, or JSON files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Transcripts are saved locally under ~/voice-transcriber/transcripts by default; original audio is saved only when requested.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill.lock.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
