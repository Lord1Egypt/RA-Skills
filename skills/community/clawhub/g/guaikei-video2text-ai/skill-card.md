## Description:

This command skill converts video URLs or local video files into cleaned transcript text and prompt-guided summaries, rewrites, highlights, scene outlines, or Chinese-English translations using the GuaiKei cloud service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, creators, content operations teams, and developers use this skill to turn selected video or audio sources into transcript text, summaries, rewrites, meeting notes, translations, and other reusable content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected videos, prompts, the service token, and some filename or path metadata may be sent to GuaiKei and its cloud upload workflow.

Mitigation: Use only media approved for third-party cloud processing, and review the provider's retention, deletion, privacy, and billing terms before sending sensitive content.

Risk: The skill can fetch broad user-supplied URLs before uploading media for processing.

Mitigation: Use trusted public video URLs or local files, and block untrusted, internal, or private-network URLs in deployment policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-video2text-ai)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [GuaiKei service website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown written to stdout, with progress and logs written to stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; accepts a video URL, local video path, or prior task ID plus an optional prompt.]

## Skill Version(s):

1.0.0 (source: evidence.release.version, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
