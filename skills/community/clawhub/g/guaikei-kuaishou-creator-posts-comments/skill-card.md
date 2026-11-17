## Description:

Processes video files and links through the GuaiKei service to produce transcriptions, summaries, and rewritten text; the inspected package does not provide the advertised Kuaishou post and comment collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and developers can provide a video file or public video link for transcription, summarization, or text rewriting. Do not use this package to collect Kuaishou creator posts or comments: that advertised capability is not present in the inspected artifact.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The title advertises Kuaishou post and comment collection, but the inspected package instead processes videos for transcription and content generation.

Mitigation: Do not install it for Kuaishou data collection; verify the needed capability before use.

Risk: Video files supplied to the skill are uploaded for remote processing.

Mitigation: Provide only videos or local files you are comfortable uploading to the provider's service.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/engheng-art/skills/guaikei-kuaishou-creator-posts-comments)
- [GuaiKei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown, according to the requested video-processing task]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a GuaiKei API token and access to the remote service; processes one video per command.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; bundled files state 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
