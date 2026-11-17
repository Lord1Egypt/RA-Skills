## Description:

Extracts clean video transcripts from local video files or public video links and can use a custom prompt to produce summaries, rewrites, quote extraction, translations, meeting notes, and other derived copy.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, content teams, and external users can use this command skill to turn a chosen local video file or public video URL into a transcript or prompt-directed written output such as a summary, social-media rewrite, key quotes, translation, course notes, or meeting minutes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A chosen local path can be uploaded to the GuaiKei service and storage provider.

Mitigation: Only pass video files that the user explicitly selected for upload; avoid sensitive local paths and require human confirmation before using a path supplied by another page, prompt, or collaborator.

Risk: A chosen URL can be fetched and processed without strong host, media-type, or size restrictions.

Mitigation: Use only trusted public video URLs and avoid private, internal, or very large remote files until host restrictions, size limits, and media validation are added.

Risk: The service requires an API token and sends selected media to an external service.

Mitigation: Configure GUAIKEI_API_TOKEN through the environment, do not expose it in prompts or logs, and install the skill only where sending selected media to GuaiKei is acceptable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-video-transcript-extractor)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [GuaiKei service website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or prompt-directed prose printed to stdout, with progress and diagnostic messages printed separately to stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0 or newer and the GUAIKEI_API_TOKEN environment variable; accepts a local file path, a public video URL, or a prior task ID plus an optional prompt.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
