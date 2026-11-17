## Description:

PhoenixClaw is a passive journaling skill that scans daily conversations from all configured session paths via cron to generate markdown journals using semantic understanding.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goforu](https://clawhub.ai/user/goforu)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use PhoenixClaw to automate daily, weekly, and long-term personal journaling from OpenClaw sessions, memory files, and selected media. It can summarize activity, identify patterns, update profile and growth-map files, and support manual journal regeneration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read broad private conversation history and memory files for passive journaling.

Mitigation: Install only when passive scheduled journaling is desired, review the configured read paths, and choose a journal path appropriate for private records.

Risk: Long-term profile, growth-map, timeline, and media records can retain sensitive personal context.

Mitigation: Review profile and growth-map updates before relying on them, avoid preserving sensitive media or EXIF/GPS data, and keep journal storage under the user's retention controls.

Risk: The rolling-journal script includes an unsafe local shell fallback around configured paths.

Mitigation: Remove the execSync shell fallbacks or strictly validate journal_path before enabling cron or unattended execution.

Risk: Optional plugins can process personal moments, media, or finance-related screenshots.

Mitigation: Disable unwanted plugins and review plugin behavior before allowing their output into daily journals.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/goforu/skills/phoenixclaw)
- [User configuration](references/user-config.md)
- [Cron setup](references/cron-setup.md)
- [Media handling](references/media-handling.md)
- [Plugin protocol](references/plugin-protocol.md)
- [Obsidian format](references/obsidian-format.md)
- [Profile evolution](references/profile-evolution.md)
- [Skill recommendations](references/skill-recommendations.md)
- [Visual design](references/visual-design.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown journal files with supporting configuration and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May copy selected media into journal assets and update timeline, profile, and growth-map files in user-configured paths.]

## Skill Version(s):

0.0.19 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
