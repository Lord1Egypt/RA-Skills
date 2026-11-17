## Description:

Transcribes video or audio from local files or supported public links into cleaned text and can use a custom prompt to produce summaries, rewrites, quotes, shot scripts, or translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External content creators, content operations teams, and developers use this skill to turn a supplied video URL, local media file, or prior GuaiKei task ID into reusable transcript, summary, content rewrite, meeting notes, or translation text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media files, URLs, prompts, and task identifiers may be sent to GuaiKei's cloud service, and file, URL, or upload destinations are not tightly scoped.

Mitigation: Use only media files and links intended for GuaiKei processing, avoid sensitive local paths, and run untrusted URLs in a contained environment with restricted filesystem and network access.

Risk: Privacy and deletion claims are provider promises rather than guarantees enforced by this client.

Mitigation: Avoid regulated or confidential media unless the provider terms and operational controls have been separately reviewed and approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-video-transcript)
- [GuaiKei service website](https://www.guaikei.com)
- [node-downloader-helper reference](https://github.com/hgouveia/node-downloader-helper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with shell commands; the runtime command returns generated transcript or prompt-directed text on stdout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires GUAIKEI_API_TOKEN; progress and errors are emitted on stderr.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
