## Description:

Md To Share converts Markdown files into shareable long-image JPEG or PNG outputs for agents such as OpenClaw and Claude Code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dtacheng](https://clawhub.ai/user/dtacheng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn Markdown reports, notes, or responses into image files for sharing on Discord, WeChat, iMessage, or local channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Markdown is rendered as live browser content in headless Chromium.

Mitigation: Convert trusted Markdown, sanitize HTML, or block network access when handling untrusted files.

Risk: Installation downloads Playwright Chromium during setup.

Mitigation: Install in a controlled environment and review the dependency and browser download before deployment.

Risk: Generated images may be sent to an unintended platform or expose sensitive Markdown content.

Mitigation: Confirm the target channel and review generated files before sending them externally.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dtacheng/skills/md-to-share)
- [Skill Definition](artifact/SKILL.md)
- [README](artifact/README.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Guidance]

**Output Format:** [JPEG or PNG image files plus terminal status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May split long or large images into numbered output files for channel constraints.]

## Skill Version(s):

2.2.0 (source: SKILL.md frontmatter and server release metadata; package.json lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
