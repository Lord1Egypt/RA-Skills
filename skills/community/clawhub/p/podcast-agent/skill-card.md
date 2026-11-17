## Description:

Search articles on any topic, generate a two-host dialogue script, and synthesize podcast audio via TTS. Turn long reads into listenable content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[besty0121](https://clawhub.ai/user/besty0121)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-producing agents use this skill to turn article research into a conversational podcast script and synthesized MP3 audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Article URL fetching may be redirected toward internal services.

Mitigation: Use only in an environment where arbitrary article URLs cannot reach sensitive internal services, and harden redirect handling before broader deployment.

Risk: Podcast source text may be processed by edge-tts/Microsoft TTS services.

Mitigation: Avoid private or proprietary text unless external TTS processing is acceptable for that content.

Risk: Dependency and output-path handling need deployment review.

Mitigation: Prefer pinned dependencies and hardened output-path handling before installing or automating the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/besty0121/skills/podcast-agent)
- [Publisher profile](https://clawhub.ai/user/besty0121)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance, audio files]

**Output Format:** [Markdown guidance with JSON script examples, shell commands, and generated MP3 files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Podcast audio is written as MP3 output; script examples use a title, duration estimate, and speaker segments.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
