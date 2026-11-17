## Description:

Transcribes local videos and supported video links into cleaned text, with optional prompt-directed summaries, rewrites, quote extraction, shot breakdowns, and Chinese-English translation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT

## Use Case:

Content creators, editors, and teams use this command-line skill to transcribe videos, prepare meeting or course notes, and create prompt-directed summaries or repurposed copy from local videos or supported links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill's documented network and encryption assurances do not match the handling of video files, so confidential recordings may be exposed to unverified storage or processing destinations.

Mitigation: Before sending confidential recordings, confirm actual storage destinations and retention/no-training terms with the publisher; use non-sensitive media until verified.

Risk: A video supplied through an insecure source link may be exposed during retrieval.

Mitigation: Prefer HTTPS source links.

Risk: Video downloads or cached copies may remain locally, and cleanup in the skill's temporary directory could affect unrelated files placed there.

Mitigation: Keep the skill's temporary directory isolated from unrelated files and review/remove cached copies after processing.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/engheng-art/skills/guaikei-video-gist)
- [Publisher service and token information](https://www.guaikei.com/)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain text or Markdown, depending on the requested task]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cleaned transcription or prompt-directed written content]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
