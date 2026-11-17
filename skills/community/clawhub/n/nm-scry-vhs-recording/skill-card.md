## Description:

Generates terminal recordings using VHS tape scripts and produces GIF outputs

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the skill to create terminal-session recordings for documentation and demos by validating VHS tape files and generating GIFs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Tape commands execute with the user's host permissions.

Mitigation: Review tape contents and commands before running; only execute tapes you trust on the current host.

Risk: The guide includes a public publishing option, and recordings may contain sensitive content.

Mitigation: Use public publishing only when intended, and inspect recordings for sensitive content before publishing.

## Reference(s):

- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/scry)
- [ClawHub release](https://clawhub.ai/athola/skills/nm-scry-vhs-recording)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [GIF terminal recordings, with VHS tape instructions and shell commands in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The tape file specifies the output path; VHS also supports MP4 and WebM.]

## Skill Version(s):

1.10.3 (source: artifact frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
