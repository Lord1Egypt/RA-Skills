## Description:

Operates and troubleshoots the OpenClaw CLI across setup, gateway and node lifecycle, channel login, messaging, agent turns, models, plugins, and system health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ramensushi2026](https://clawhub.ai/user/ramensushi2026)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to select, run, and troubleshoot OpenClaw CLI commands while preserving profile isolation and verifying outcomes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing or updating from an unpinned source can introduce unreviewed skill behavior.

Mitigation: Prefer a tagged or pinned commit from a trusted repository and review changes before updating.

Risk: Reset, uninstall, force, credential-clearing, message delivery, plugin, cron, or update commands can affect local data, credentials, messages, or runtime state.

Mitigation: Require explicit confirmation for these command classes, inspect command help before risky operations, and verify outcomes with status, health, doctor, logs, or command-specific checks.

Risk: Mixing default, development, and named profiles can operate on the wrong OpenClaw state.

Mitigation: Select the runtime scope before running commands, keep profile usage consistent across the workflow, and use profile-specific verification commands.

## Reference(s):

- [OpenClaw CLI Command Map](references/command-map.md)
- [OpenClaw CLI Docs](https://docs.openclaw.ai/cli)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend JSON CLI output for automation and explicit post-check commands.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
