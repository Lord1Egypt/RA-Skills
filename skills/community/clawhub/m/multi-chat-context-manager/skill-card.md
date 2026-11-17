## Description:

CLI tool to store and retrieve conversation contexts per channel/user.

This skill is ready for commercial/non-commercial use.

## Publisher:

[derick001](https://clawhub.ai/user/derick001)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to manually save, retrieve, list, and clear conversation context keyed by channel, user, and thread identifiers. It is useful when scripts or custom integrations need lightweight local context persistence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved conversation history is stored locally in plaintext JSON.

Mitigation: Avoid storing secrets, regulated data, or sensitive customer information; restrict filesystem access to the skill directory.

Risk: The list command exposes all saved contexts to the caller.

Mitigation: Run list only in trusted sessions and review output before sharing logs or terminal transcripts.

Risk: The clear command without a channel removes all stored contexts.

Mitigation: Use channel, user, and thread filters when clearing specific records, and keep backups if context loss would be disruptive.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/derick001/skills/multi-chat-context-manager)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration]

**Output Format:** [JSON command output and concise CLI guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores conversation context locally in plaintext JSON under the skill data directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter states 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
