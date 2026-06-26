## Description: <br>
Automatically fetch, transcribe, and archive Hacker News podcast episodes (Hacker News Morning Brief). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to set up a local podcast ingestion workflow that downloads RSS episodes, transcribes audio with Whisper, and archives searchable Markdown transcripts. It is aimed at Hacker News Morning Brief by default and can also be pointed at another podcast RSS feed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads podcast audio and stores transcripts locally, which can consume disk space over time. <br>
Mitigation: Use a dedicated archive directory, monitor disk usage, and use --limit when testing or when pointing the skill at a new feed. <br>
Risk: The workflow depends on local Whisper and ffmpeg installations and performs local transcription work. <br>
Mitigation: Install Whisper and ffmpeg from trusted sources and choose a Whisper model appropriate for the machine's performance and accuracy needs. <br>
Risk: Optional scheduling can repeatedly fetch new episodes without further prompts. <br>
Mitigation: Enable cron or OpenClaw scheduling only when ongoing automatic downloads are intended. <br>


## Reference(s): <br>
- [HN Podcast Archive Directory Layout](references/archive-layout.md) <br>
- [Hacker News Morning Brief RSS feed](https://media.rss.com/hacker-news-morning-brief/feed.xml) <br>
- [FFmpeg](https://ffmpeg.org) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Markdown, Text, Files] <br>
**Output Format:** [Markdown guidance with bash commands; runtime outputs include audio files, text transcripts, transcript.md files, metadata.json files, and state.json.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local archive paths, RSS feed URLs, Whisper model names, and optional per-run episode limits.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
