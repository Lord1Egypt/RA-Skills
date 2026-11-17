## Description:

Transcribes video links or local video files into cleaned copy and can use custom prompts to summarize, rewrite, extract quotes, outline scenes, or translate the content through the GuaiKei cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content creators, editors, and developers use this skill to turn public video URLs or local media into transcripts, summaries, rewritten copy, quote extractions, scene outlines, translations, meeting notes, or content drafts. It requires a GuaiKei API token and sends selected media to the vendor cloud service for processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch arbitrary URLs and upload any readable local file to cloud storage without enough scoping or confirmation.

Mitigation: Review before installing, use only videos intentionally meant for vendor-cloud processing, run from a low-privilege account, limit access to intended media files, and avoid private or internal URLs.

Risk: The --id last option reuses a prior video-analysis task.

Mitigation: Treat --id last as prior-task reuse; use explicit task IDs when task separation matters and avoid relying on it across unrelated media.

Risk: The current release lacks stronger controls called out by the security guidance.

Mitigation: Publisher should add confirmation prompts, media validation, private-network blocking, upload host allowlisting, size limits, and clearer disclosure of storage destinations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-video-copywriting-extractor)
- [GuaiKei service homepage](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text on stdout, with progress and errors on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; accepts either --file or --id plus an optional --prompt.]

## Skill Version(s):

1.0.0 (source: server release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
