## Description:

Transcribes local video or audio files and public media links into readable text, with optional prompts for summaries, rewrites, quotes, and translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and teams use the skill to turn recorded videos, audio, or public media links into transcripts, summaries, meeting notes, and reusable copy. A GuaiKei API token and cloud processing are required.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media, media URLs, prompts, and the API token are sent to the GuaiKei cloud service and potentially its presigned upload storage.

Mitigation: Use only media and prompts approved for cloud processing, and protect the API token.

Risk: Provider retention and deletion claims are not enforced by the local skill package.

Mitigation: Avoid confidential media unless the provider's retention and deletion terms meet your requirements.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/engheng-art/skills/guaikei-ai-video-subtitle)
- [GuaiKei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or prompt-directed structured text on standard output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports transcripts, summaries, rewrites, quote extraction, and translation; progress messages go to standard error.]

## Skill Version(s):

1.0.0 (source: ClawHub release, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
