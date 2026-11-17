## Description:

Summarize podcast episodes from Spotify, Apple Podcasts, or RSS feeds. Extracts transcripts and generates summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daaab](https://clawhub.ai/user/daaab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and podcast users use this skill to fetch podcast audio from supported episode, feed, or audio URLs, transcribe it with Whisper, and produce a transcript or structured summary.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted podcast URLs or RSS feeds can trigger arbitrary remote fetches and large audio downloads.

Mitigation: Use trusted podcast URLs or feeds, run in an isolated environment, and apply network egress controls and resource limits.

Risk: Transcript text may be sent to Gemini or OpenAI when API keys are configured.

Mitigation: Do not process private or sensitive audio unless sharing transcript text with the configured external provider is acceptable.

## Reference(s):

- [Podcast Summarizer ClawHub page](https://clawhub.ai/daaab/skills/podcast-summarizer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown transcript and summary output, optionally written to a file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Summary length can be short, medium, or long; transcript-only output is supported.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
