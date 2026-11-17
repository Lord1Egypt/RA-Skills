## Description:

OpenClaw interface localization skill for translating the OpenClaw Web Control UI and Chrome extension interface into Chinese.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zoranke](https://clawhub.ai/user/zoranke)

### License/Terms of Use:


## Use Case:

OpenClaw users and developers use this skill to apply Chinese translations to the OpenClaw Web Control UI and Chrome extension interface. It is intended for localization of an existing OpenClaw installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill modifies files in a global OpenClaw installation.

Mitigation: Run the translation script with --dry-run first and confirm the target path before applying changes.

Risk: Translation changes can be overwritten by OpenClaw updates or may need elevated file permissions.

Mitigation: Use the script's backup and --restore behavior, and avoid elevated privileges unless the OpenClaw install path requires them.

Risk: The documented reinstall command is broad and unpinned.

Mitigation: Review the installed OpenClaw version before reinstalling and prefer the backup restore path when reverting translations.

## Reference(s):

- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [Openclaw Zh ClawHub release](https://clawhub.ai/zoranke/skills/openclaw-zh)
- [Publisher profile](https://clawhub.ai/user/zoranke)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and file path guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes localization mappings and guidance for applying, previewing, and restoring translations.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
