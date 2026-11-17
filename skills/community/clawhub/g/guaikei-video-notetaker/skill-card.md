## Description:

Transcribes local or linked video and audio into readable text and can produce summaries, rewrites, quotes, scripts, or translations from a custom prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators and business teams use this skill to turn existing video or audio into transcripts, meeting notes, summaries, and reusable copy. It accepts a local media file or video URL and can tailor the resulting text to a prompt.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media, URLs, prompts, task IDs, and the service token are sent to a third-party service and its upload destination.

Mitigation: Use only approved, non-sensitive media and a scoped service token; obtain approval before processing confidential or regulated content.

Risk: The skill can fetch arbitrary URLs, including private-network or local addresses.

Mitigation: Supply only reviewed public media URLs; do not provide localhost or internal-network links.

Risk: Reusing a prior task ID may expose unintended previous media context.

Mitigation: Confirm the intended task before requesting a follow-up; avoid reusing prior tasks across sensitive workflows.

Risk: Large files and long videos may incur substantial processing costs.

Mitigation: Check media duration and expected charges before submitting large files.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/engheng-art/skills/guaikei-video-notetaker)
- [Guaikei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [Plain text transcript or prompt-directed prose]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can return summaries, rewrites, quotes, scripts, or translations instead of a transcript when prompted.]

## Skill Version(s):

1.0.0 (source: package.json and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
