## Description:

Search, install, and export agentars from the CatchClaw marketplace. Use when the user wants to find, install, or package agent templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lovelcp](https://clawhub.ai/user/lovelcp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use CatchClaw to search marketplace agentars, install selected agent templates, export local agents as distributable ZIP archives, and roll back overwritten OpenClaw workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer downloads and runs remote code without release integrity verification.

Mitigation: Do not run install.sh unless the publisher adds integrity verification; inspect the bundled CLI and any downloaded agentars before use.

Risk: Install and rollback workflows can write to OpenClaw workspaces and may overwrite the main workspace when explicitly selected.

Mitigation: Evaluate with a disposable OpenClaw profile, prefer named installs, avoid --overwrite, and use rollback --latest only after reviewing the target backup.

Risk: Registry and home-directory overrides can redirect marketplace operations or change where configuration is written.

Mitigation: Keep registry endpoints pinned to trusted HTTPS URLs and review AGENTAR_API_BASE_URL and AGENTAR_HOME before running commands.

Risk: Exported agentar ZIP archives and optional API-key installs can include sensitive operational context if misused.

Mitigation: Avoid --api-key unless required, keep MEMORY.md excluded unless explicitly needed, and inspect exported ZIPs for unexpected files or secrets.

## Reference(s):

- [CatchClaw ClawHub listing](https://clawhub.ai/lovelcp/skills/install)
- [CatchClaw homepage](https://github.com/OpenAgentar/catchclaw)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce installed workspace files, exported agentar ZIP archives, backups, and optional credentials files depending on user-selected commands.]

## Skill Version(s):

3.5.8 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
