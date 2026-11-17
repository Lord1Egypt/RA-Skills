## Description:

Transcribes existing videos from local files or public links and creates summaries, subtitles, notes, or rewritten copy using an optional prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Creators, editors, and teams use this skill to turn existing videos into transcripts, subtitles, summaries, meeting notes, and platform-specific copy.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Video links may fetch content from arbitrary URLs, including internal or private-network addresses.

Mitigation: Use only approved public video links; avoid internal URLs, localhost, and private-network addresses.

Risk: Selected videos, downloaded content, and prompts are sent to remote services using an API token; provider retention and privacy claims are unverified.

Mitigation: Avoid confidential, proprietary, or regulated recordings unless the provider's handling and retention terms have been independently verified.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/engheng-art/skills/guaikei-video-text-generator)
- [GuaiKei website](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain text or prompt-directed formatted text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Output may be a transcript, subtitle text, summary, or rewritten copy; a prior task ID can be reused.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; bundled files declare 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
