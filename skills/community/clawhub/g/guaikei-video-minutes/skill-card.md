## Description:

Transcribes local or public-link video and audio into cleaned text and can generate summaries, meeting minutes, rewrites, and translations from a custom prompt.

This skill is ready for commercial/non-commercial use.

## Publisher:

[engheng-art](https://clawhub.ai/user/engheng-art)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, teams, and developers use this skill to transcribe recordings or turn video and audio into summaries, meeting minutes, and other reusable copy through a paid cloud service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected media, links, and prompts are sent to a paid third-party cloud service.

Mitigation: Confirm the content is approved for sharing and accept service charges before running the skill.

Risk: Private, internal, authenticated, or credential-bearing URLs may expose sensitive content.

Mitigation: Do not supply those URLs unless you intend the agent to fetch and upload their content.

Risk: Server-side retention and deletion promises cannot be confirmed by the local skill.

Mitigation: Treat deletion claims as provider policy and verify retention terms before processing sensitive material.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/engheng-art/skills/guaikei-video-minutes)
- [GuaiKei service](https://www.guaikei.com)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Plain text or prompt-directed structured text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Cleaned transcription by default; custom prompts can request summaries, rewrites, or translations.]

## Skill Version(s):

1.0.0 (source: ClawHub release and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
