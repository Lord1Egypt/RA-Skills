## Description:

Summarize podcast episodes into concise, actionable insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hughtan93-dev](https://clawhub.ai/user/hughtan93-dev)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to turn podcast episodes from local audio, URLs, YouTube, RSS feeds, or podcast pages into concise structured summaries with key points, action items, timestamps, and relevant links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full functionality depends on external transcription and download tools that may require installation.

Mitigation: Use a virtual environment and install reviewed, pinned packages for tools such as yt-dlp and Whisper before use.

Risk: Podcast audio can contain private or sensitive information if transcribed with an external API.

Mitigation: Avoid sending sensitive recordings to external APIs unless explicitly intended; use a local transcription option when privacy is required.

## Reference(s):

- [Podcast Summarize Technical Reference](references/technical.md)
- [ClawHub Skill Page](https://clawhub.ai/hughtan93-dev/skills/podcast-summarize)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can include title metadata, key points, detailed summary paragraphs, action items, timestamps, related links, and follow-up questions.]

## Skill Version(s):

0.1.0 (source: release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
