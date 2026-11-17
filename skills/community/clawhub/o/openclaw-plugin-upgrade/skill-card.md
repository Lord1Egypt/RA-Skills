## Description:

OpenClaw Plugin Upgrade helps agents upgrade general OpenClaw plugins and provides a focused upgrade path for the QQ bot plugin, including version targeting, file verification, compatibility handling, rollback, and gateway restart support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ryanlee-gemini](https://clawhub.ai/user/ryanlee-gemini)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to upgrade installed OpenClaw plugins from an agent session, especially @tencent-connect/openclaw-qqbot. It is intended for controlled maintenance workflows where plugin package names, versions, and cleanup paths are known and trusted.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill changes installed OpenClaw plugins and can restart the gateway.

Mitigation: Use it only in environments where plugin maintenance and gateway restart are expected, and use the no-restart option when restart timing must be controlled.

Risk: The upgrade flow gives broad control over package selection, cleanup paths, and package-supplied code.

Mitigation: Use exact trusted package names and versions, avoid arbitrary legacy directory values, and review or fix the script before using it near important local files or credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ryanlee-gemini/skills/openclaw-plugin-upgrade)
- [Publisher profile](https://clawhub.ai/user/ryanlee-gemini)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and structured command output fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The upgrade script emits fields such as PLUGIN_NEW_VERSION, PLUGIN_ID, and PLUGIN_REPORT for agent-facing status reporting.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
