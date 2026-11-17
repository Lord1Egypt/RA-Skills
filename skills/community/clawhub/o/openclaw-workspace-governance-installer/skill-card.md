## Description:

Install OpenClaw WORKSPACE_GOVERNANCE in minutes. Get guided setup, upgrade checks, migration, and audit for long-running workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adamchanadam](https://clawhub.ai/user/adamchanadam)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and workspace operators use this skill to install and maintain OpenClaw workspace governance, including setup, migration, audit, safe configuration edits, and upgrade checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The quick-start install command uses an unpinned external plugin version, which can change over time.

Mitigation: Review the linked plugin source and prefer a pinned, reviewed version instead of @latest before installation.

Risk: The governance plugin can modify OpenClaw workspace configuration and related governance files.

Mitigation: Install only when the publisher is trusted and the workspace owner is comfortable granting that authority; use the documented audit and rollback-oriented flows to review changes.

Risk: The skill includes an experimental controlled-UAT flow for applying BOOT upgrade proposals.

Mitigation: Use proposal application only with explicit human approval and review generated proposals before applying them.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/adamchanadam/skills/openclaw-workspace-governance-installer)
- [OpenClaw WORKSPACE_GOVERNANCE](https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE)
- [English README](https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/README.md)
- [Governance Handbook (EN)](https://github.com/Adamchanadam/OpenClaw-WORKSPACE-GOVERNANCE/blob/main/WORKSPACE_GOVERNANCE_README.en.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and OpenClaw command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes command sequences and chat commands for installation, upgrade, migration, audit, configuration edits, uninstall, and controlled upgrade proposal workflows.]

## Skill Version(s):

0.2.9 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
