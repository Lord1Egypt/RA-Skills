## Description:

Complete Omi.me integration for memories, action items (tasks), and conversations with full CRUD and sync capabilities for OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caioiscoding](https://clawhub.ai/user/caioiscoding)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to configure Omi.me API access and manage memories, action items, conversations, and sync operations from shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The shell scripts handle Omi.me API tokens and include a command that can print the configured token.

Mitigation: Avoid printing tokens, review token-handling code before installation, and ensure ~/.config/omi-me is mode 700 and the token file is mode 600 on every write path.

Risk: Request destination handling needs review before use.

Mitigation: Replace API_URL with OMI_API_URL where needed and verify the Omi.me API endpoint before running commands.

Risk: Delete and sync commands operate on Omi.me memories, tasks, and conversations.

Mitigation: Treat delete and sync operations as sensitive actions and review intended data impact before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caioiscoding/skills/omi-me)
- [Omi.me](https://omi.me)
- [Omi.me developer API overview](https://docs.omi.me/doc/developer/api/overview)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires OMI_API_TOKEN and the omi and omi-token shell commands.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
