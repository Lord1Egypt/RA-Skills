## Description:

Converts local or online videos into cleaned text transcripts and optional prompt-driven summaries, rewrites, highlights, subtitles, or translations through the GuaiKei service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

External users, content teams, and developers use this command skill to turn video or audio sources into reusable text for transcripts, meeting notes, course summaries, social copy, highlights, and translation workflows. It requires a GUAIKEI_API_TOKEN and sends selected videos and prompts to the GuaiKei service for processing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can fetch and upload arbitrary reachable URLs without strong private-address, redirect, size, or duration limits.

Mitigation: Use only trusted video URLs, avoid running it from networks with access to internal services, and require URL, redirect, size, and timeout controls before broader deployment.

Risk: Selected videos, prompts, and token-backed requests are sent to an external service.

Mitigation: Use only content approved for external processing, protect GUAIKEI_API_TOKEN as a secret, and confirm service data handling terms before using sensitive media.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/engheng-art/skills/guaikei-video-to-text)
- [Publisher profile](https://clawhub.ai/user/engheng-art)
- [GuaiKei service site](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown emitted to stdout, with progress and logs emitted to stderr]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output content depends on the optional prompt; without a prompt the skill returns a cleaned transcript.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
