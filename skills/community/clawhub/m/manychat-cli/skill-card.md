## Description:

Agent-friendly ManyChat automation CLI with playbook support for multi-step workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danielfoch](https://clawhub.ai/user/danielfoch)

### License/Terms of Use:


## Use Case:

Developers and automation operators use this skill to run ManyChat subscriber lookup, tagging, custom field updates, content sends, and JSON playbook workflows from an agent-controlled CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can update live subscriber data, apply tags, set custom fields, create or update subscribers, and send flows or content.

Mitigation: Review playbooks and command arguments before execution, require explicit approval for subscriber mutations or sends, and target only intended subscribers.

Risk: API credentials could be exposed or sent to an unintended host when using API key arguments or overriding the ManyChat base URL.

Mitigation: Use a least-privilege API key, prefer environment-based secret handling, and only use MANYCHAT_BASE_URL or --base-url with trusted HTTPS test services and test credentials.

## Reference(s):

- [ManyChat CLI on ClawHub](https://clawhub.ai/danielfoch/skills/manychat-cli)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [sample_playbook.json](artifact/sample_playbook.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions, Python and shell code, and JSON CLI output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands require a ManyChat API key and may use an optional trusted ManyChat API base URL.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
