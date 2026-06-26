## Description: <br>
Build and operate an automated archive workflow for the Hacker News podcast/feed: detect new episodes from RSS, download audio, transcribe locally with Whisper, generate markdown archives with metadata, and keep an index/history for repeatable ingestion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to set up and maintain an RSS-based podcast archive that downloads episodes, runs local Whisper transcription, and writes searchable markdown records with index and state files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill downloads audio from a user-selected RSS feed and writes archive files to disk. <br>
Mitigation: Use a trusted feed URL, test first with --limit or --dry-run, and point --output-dir at a dedicated archive directory. <br>
Risk: Local transcription and recurring automation can consume disk, CPU, and runtime unexpectedly. <br>
Mitigation: Confirm ffmpeg, whisper, and feedparser installations from trusted sources, check disk usage during initial runs, and schedule automation only after manual validation. <br>


## Reference(s): <br>
- [Archive layout](references/layout.md) <br>
- [OpenClaw automation template](references/openclaw-automation.md) <br>
- [ClawHub skill page](https://clawhub.ai/terrycarter1985/hn-podcast-archive) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, Python script behavior, JSON state, JSONL run logs, downloaded files, transcripts, and per-episode markdown archives] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes audio, transcript, episode markdown, index.md, state.json, and run-log.jsonl under the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
