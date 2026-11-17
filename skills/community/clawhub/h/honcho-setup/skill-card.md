## Description:

Installs and configures the Honcho OpenClaw plugin for long-term agent memory, including optional migration of existing workspace memory files to Honcho and gateway restart guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ajspig](https://clawhub.ai/user/ajspig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add Honcho-backed long-term memory and migrate existing memory files with explicit confirmation before upload.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace memory files and future workspace conversations may be sent to Honcho or a configured endpoint while the plugin is enabled.

Mitigation: Install only after reviewing the destination, use a trusted HTTPS endpoint, avoid entering secrets in monitored conversations, and disable the plugin when ongoing memory capture is not desired.

Risk: The Honcho API key is stored in ~/.openclaw/openclaw.json.

Mitigation: Protect local OpenClaw configuration, avoid sharing it, and rotate or revoke the API key if the file may have been exposed.

Risk: Migration can upload existing memory and workspace context files to an external service.

Mitigation: Review the setup prompt's file list and destination before confirming; skip migration if the workspace contains sensitive content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ajspig/skills/honcho-setup)
- [Publisher profile](https://clawhub.ai/user/ajspig)
- [Honcho homepage](https://honcho.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides installation, setup, status checks, and disabling ongoing Honcho observation.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
