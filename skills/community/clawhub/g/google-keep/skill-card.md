## Description:

Read, create, edit, search, and manage Google Keep notes and lists via CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tag-assistant](https://clawhub.ai/user/tag-assistant)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to manage Google Keep notes and lists from an agent-assisted CLI, including reading, creating, editing, searching, labeling, and exporting notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses long-lived Google master tokens with broad account access, creating credential-exposure risk.

Mitigation: Use it only on a private, trusted machine; treat the token like a password; avoid placing tokens in shell history; and prefer interactive secret entry or a secure credential store.

Risk: Credentials and synced note state are cached in the skill directory.

Mitigation: Keep the skill directory and backups private, do not commit the .config directory, and verify local credential files remain restricted to the current user.

Risk: The skill relies on unofficial Google Keep access through gkeepapi and gpsoauth, so compatibility can change without notice.

Mitigation: Test on non-critical notes first, maintain exports or backups before bulk changes, and review dependency updates before use.

## Reference(s):

- [ClawHub Google Keep skill page](https://clawhub.ai/tag-assistant/skills/google-keep)
- [gkeepapi project](https://github.com/kiwiz/gkeepapi)
- [gpsoauth project](https://github.com/simon-weber/gpsoauth)
- [Google Embedded Setup](https://accounts.google.com/EmbeddedSetup)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI output is human-readable text or JSON when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can read and modify Google Keep content after authentication; stores credentials and cached state locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
