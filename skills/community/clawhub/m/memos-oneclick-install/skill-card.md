## Description:

Installs, configures, upgrades, and troubleshoots the MemOS local memory plugin for OpenClaw agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mathematics-yang](https://clawhub.ai/user/mathematics-yang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to add persistent local memory, semantic retrieval, task summaries, and memory-management tools to an OpenClaw agent. It guides the agent through install, configuration, upgrade, verification, and basic troubleshooting while asking the user only for embedding-model details when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives the agent broad authority to install npm packages, modify OpenClaw configuration, restart services, and repair installations automatically.

Mitigation: Review the skill and package source before use, run it only in an environment where those changes are acceptable, and inspect configuration changes after installation.

Risk: Fallback installer paths use remote shell scripts.

Mitigation: Prefer the OpenClaw CLI or another pinned, verified package source; avoid pipe-to-shell installers unless the script source has been reviewed and trusted.

Risk: The installed plugin stores conversation memory locally and may interact with external embedding APIs if configured.

Mitigation: Use local embeddings for sensitive work, store API keys through environment-variable references when possible, and check telemetry, sharing, and memory-capture settings before enabling the plugin.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mathematics-yang/skills/memos-oneclick-install)
- [MemOS for OpenClaw Homepage](https://memos-claw.openmem.net)
- [MemOS for OpenClaw Documentation](https://memos-claw.openmem.net/docs/)
- [MemOS for OpenClaw Troubleshooting](https://memos-claw.openmem.net/docs/troubleshooting.html)
- [NPM Package](https://www.npmjs.com/package/@memtensor/memos-local-openclaw-plugin)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing installation and troubleshooting steps; the installed plugin may persist local conversation memory.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
