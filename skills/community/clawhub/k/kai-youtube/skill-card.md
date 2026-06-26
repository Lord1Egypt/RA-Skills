## Description: <br>
Download and transcribe YouTube videos using yt-dlp and Whisper CLI, saving audio and transcripts for playback and summary from any YouTube URL. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ogdegenblaze](https://clawhub.ai/user/ogdegenblaze) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to download audio from a YouTube URL, transcribe it locally with Whisper, and save the transcript for review or summarization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads YouTube audio and stores both audio and transcripts on disk. <br>
Mitigation: Use trusted YouTube links, monitor disk usage for long videos, and delete saved media or transcripts when they are no longer needed. <br>
Risk: Local transcription can take several minutes and may produce imperfect text for long, noisy, or multilingual videos. <br>
Mitigation: Check video length before running the workflow and review the transcript before relying on it for summaries or decisions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, files] <br>
**Output Format:** [Plain text transcript with shell command output and saved MP3/TXT files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires yt-dlp and Whisper CLI; stores audio and transcript files under kai-yt-videos by video ID.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
