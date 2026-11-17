## Description:

Converts local video files or public video links into cleaned transcripts and structured writing such as summaries, rewrites, quotes, scene scripts, and translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, content teams, and developers use this skill to turn completed videos or audio/video links into reusable written content. It supports transcription, summarization, content analysis, style rewrites, quote extraction, meeting notes, course breakdowns, and translation through a custom prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video files, prompts, task IDs, API tokens, and some file metadata are sent to the GuaiKei service and its presigned storage backend.

Mitigation: Use the skill only for content that can be shared with that provider, and independently verify provider retention and deletion commitments before using confidential videos.

Risk: User-supplied URLs may expose private network data if internal, localhost, cloud-metadata, or otherwise private URLs are provided.

Mitigation: Provide trusted public media URLs or local files, and avoid internal or private network URLs.

Risk: Large downloads may consume local temporary storage.

Mitigation: Monitor the skill temporary directory and disk usage during large video processing jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-video2text)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [GuaiKei website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown returned to stdout, with progress and logs on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0 or newer and GUAIKEI_API_TOKEN; accepts a video URL, local file path, historical task ID, and optional prompt.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
