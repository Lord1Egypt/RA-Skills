## Description: <br>
Download, transcribe, and archive Hacker News podcast episodes into a searchable local archive, with incremental processing and support for custom podcast RSS feeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to fetch podcast episodes from an RSS feed, transcribe local audio with Whisper, build a searchable archive, and search transcript text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can download media from the configured RSS feed and store audio, metadata, transcripts, Whisper models, and a search index on the local machine. <br>
Mitigation: Use trusted RSS feeds, choose an appropriate archive directory, and use --no-download when only episode metadata is needed. <br>
Risk: Running the full pipeline on large or recurring feeds can consume local storage, network bandwidth, and compute. <br>
Mitigation: Set --limit for large feeds and enable the cron example only when recurring automated processing is intended. <br>


## Reference(s): <br>
- [Default Hacker News Recap RSS feed](https://rss.buzzsprout.com/2170103.rss) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local archive files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated archives may include episode metadata JSON, audio files, transcripts, and a searchable index on disk.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
