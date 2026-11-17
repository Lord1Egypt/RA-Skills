## Description:

Convert a local video into an iPhone-compatible Live Photo package (.pvt) for Apple Photos, lock-screen wallpaper use, or Live Photo sharing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hekaiii](https://clawhub.ai/user/hekaiii)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn a local video into an Apple Photos-importable Live Photo package for sharing or iPhone lock-screen wallpaper workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted media tooling could affect the local system when the skill installs or runs ffmpeg, makelive, or pipx.

Mitigation: Install dependencies only from trusted sources and verify the tools before processing user media.

Risk: Existing .mp4, .jpg, .pvt, or .zip outputs using the same basename may be overwritten or removed.

Mitigation: Use a fresh output basename or an empty output directory for each conversion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hekaiii/skills/live-photo-maker)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local .pvt Live Photo packages and optional .zip archives for transfer.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
