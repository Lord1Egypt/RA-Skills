## Description:

Monitor Nate B Jones's YouTube channel, pull each new video transcript (YouTube captions or auto-transcribed audio), summarize it with an abstract + bullet highlights + reference links, and distribute the digest via email, chat, and/or a document per user-configured outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arpee](https://clawhub.ai/user/arpee)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, creators, and operators use this skill to monitor Nate B Jones uploads, turn new video transcripts into concise digests, and publish those digests to configured recipients or archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured email, chat, or document destinations could send digests to unintended recipients.

Mitigation: Change the example recipients and sharing settings before running, and review the first generated digest before enabling routine delivery.

Risk: Raw transcripts and scheduled run logs can accumulate retained content beyond the user's needs.

Mitigation: Set a retention policy for transcripts, audio artifacts, and audit logs before automation is enabled.

Risk: Automated polling and publishing can repeat or send stale digests if last-video tracking is misconfigured.

Mitigation: Use the configured last-video log, keep lightweight audit records, and verify duplicate prevention during initial runs.

## Reference(s):

- [Configuration example](references/config-example.yml)
- [youtube_transcript_api documentation](https://pypi.org/project/youtube-transcript-api/)
- [Whisper CLI](https://github.com/openai/whisper)
- [ClawHub skill page](https://clawhub.ai/arpee/skills/nate-b-jones-digest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown playbook with inline shell commands, configuration examples, and digest templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces concise video digest bodies and optional delivery or archival instructions; raw transcripts are retained only for traceability and are not distributed by default.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
