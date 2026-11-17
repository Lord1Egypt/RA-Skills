## Description:

Installs and configures the Honcho OpenClaw plugin so an agent can migrate local memory files and sync ongoing conversation memory with Honcho.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vvoruganti](https://clawhub.ai/user/vvoruganti)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add Honcho-backed long-term memory and personalization to an agent. The skill guides plugin installation, setup, migration of existing memory files, and verification or disabling of ongoing sync.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace memory files and ongoing conversation data may be sent to a third-party Honcho endpoint.

Mitigation: Proceed only after reviewing the disclosed destination and file list, use a self-hosted HONCHO_BASE_URL when appropriate, and disable the plugin when conversation sync is no longer desired.

Risk: The setup installs an unpinned third-party plugin that persistently handles sensitive context across sessions.

Mitigation: Prefer a reviewed and pinned plugin version, verify the package or source before enabling it, and keep the plugin disabled unless persistent memory sync is required.

Risk: Honcho API credentials are written to local OpenClaw configuration.

Mitigation: Use scoped credentials where available, protect ~/.openclaw/openclaw.json, and rotate the API key if the local configuration may have been exposed.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/vvoruganti/skills/honcho)
- [Honcho Homepage](https://honcho.dev)
- [Honcho Application](https://app.honcho.dev)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes external upload warnings, setup confirmation steps, and a command to disable ongoing Honcho sync.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
