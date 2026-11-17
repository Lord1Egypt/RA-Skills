## Description:

媒体控制专业版 helps agents configure and operate Jellyfin media-server workflows for multi-device control, user permissions, scheduled playback, media-library scans, and playback reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through Jellyfin media-server automation for home theaters and small organizations, including device control, scheduled playback, library maintenance, and reporting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording may lead agents to apply the skill to unrelated analytics, reporting, or visualization requests.

Mitigation: Use the skill only for Jellyfin and media-server automation tasks.

Risk: The skill may guide agents to run shell commands or control networked devices, including scheduled playback, library scans, ADB, Home Assistant, or local API-service actions.

Mitigation: Confirm command intent, target devices, schedules, and library-modifying actions before execution.

Risk: Configuration examples involve API keys, tokens, and local service credentials.

Mitigation: Keep secrets in environment variables or a secure secret store and avoid committing credential-bearing configuration files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/jellyfin-control-tool-pro)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown, code]

**Output Format:** [Markdown guidance with shell command examples, JSON/YAML configuration snippets, and structured JSON-style result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose command execution and networked media-device control; commands should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
