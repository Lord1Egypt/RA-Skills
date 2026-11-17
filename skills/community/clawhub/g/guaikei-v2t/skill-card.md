## Description:

guaikei-v2t converts video links or local video files into cleaned transcripts and prompt-directed outputs such as summaries, rewrites, highlights, shot breakdowns, and translations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this command skill to transcribe videos, extract subtitles or speech, summarize content, create social-media copy, generate meeting notes, and reuse prior video analysis tasks with custom prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Media content and prompts may be sent to a third-party cloud service for transcription and generation.

Mitigation: Use the skill only with media approved for third-party processing; avoid confidential, regulated, or internal-only content unless the service terms are approved.

Risk: The security scan reports that the skill can fetch arbitrary URLs and upload resulting content to a server-chosen HTTPS destination broader than the documentation discloses.

Mitigation: Avoid attacker-supplied and internal or private-network URLs; add URL allowlisting, private-network blocking, download limits, and upload-host disclosure before wider deployment.

Risk: Large or unexpected media downloads and uploads can increase cost, processing time, and exposure of user-supplied data.

Mitigation: Review media source, size, duration, and billing expectations before execution; prefer local transcription for confidential content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-v2t)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [GuaiKei service website](https://www.guaikei.com)
- [node-downloader-helper upstream project](https://github.com/hgouveia/node-downloader-helper)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text or Markdown emitted to stdout, with progress and logs on stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 16.14.0 or newer and GUAIKEI_API_TOKEN; accepts a video URL, local file path, historical task ID, and optional prompt.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
