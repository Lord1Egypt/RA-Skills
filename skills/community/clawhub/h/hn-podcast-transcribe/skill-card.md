## Description:

Download, transcribe, and archive Hacker News podcast episodes into a searchable local archive, with incremental processing and support for custom podcast RSS feeds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and podcast archivists use this skill to maintain a local searchable archive of podcast episodes by fetching RSS items, transcribing local audio with Whisper, indexing transcripts, and searching transcript snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make outbound requests to RSS feeds and feed-provided media URLs.

Mitigation: Use trusted HTTPS podcast feeds and run the skill in a restricted network or container when processing unfamiliar feeds.

Risk: The fallback downloader disables TLS certificate checks.

Mitigation: Remove the no-check-certificates behavior or avoid unattended scheduled runs until that fallback is reviewed and hardened.

Risk: Downloaded audio, episode metadata, transcript files, and search indexes are retained in a local archive.

Mitigation: Store the archive in an access-controlled directory and apply an appropriate retention policy for the podcast content being processed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/terrycarter1985/skills/hn-podcast-transcribe)
- [Default Hacker News Recap RSS feed](https://rss.buzzsprout.com/2170103.rss)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with shell commands; local transcript files in txt, srt, vtt, or json; archive metadata and index files in JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports configurable RSS feed, archive directory, Whisper model, transcript format, episode limit, and metadata-only fetching.]

## Skill Version(s):

2.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
