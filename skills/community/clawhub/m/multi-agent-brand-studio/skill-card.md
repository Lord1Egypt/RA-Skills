## Description:

Sets up Multi-Agent Brand Studio on OpenClaw for multi-brand social media operations, approval-gated publishing, brand-isolated workspaces, and multi-agent content workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kuan0808](https://clawhub.ai/user/kuan0808)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and operators use this skill to scaffold an OpenClaw-based social media operations workspace for multiple brands. It is intended for brand-aware content planning, research, drafting, review, routing, and approval workflows across a specialized agent team.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup makes lasting OpenClaw configuration, workspace, cron, and Telegram routing changes.

Mitigation: Back up ~/.openclaw/openclaw.json, review scaffold.sh and patch-config.js before execution, and run OpenClaw diagnostics after setup.

Risk: Telegram bot tokens and channel identifiers are needed for routing brand and operations messages.

Mitigation: Prefer OpenClaw secrets management for the bot token and verify channel-map routing before connecting real brand channels.

Risk: Expanded trusted local executable paths can increase local execution exposure.

Mitigation: Review trusted path changes before installation and avoid trusting broad Homebrew directories unless the local executable risk is acceptable.

Risk: Optional QMD semantic memory and image generation depend on local tooling that may be missing or unpinned.

Mitigation: Skip optional QMD or pin and verify the install; confirm optional Creator image tooling before relying on generated visual assets.

Risk: Multi-brand workflows can route approvals or context to the wrong brand if profiles, brand IDs, or channel maps are incomplete.

Mitigation: Fill brand profiles and content guidelines, keep the brand registry current, and verify the approval workflow and routing before publishing.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kuan0808/skills/multi-agent-brand-studio)
- [Architecture](references/architecture.md)
- [Agent Roles](references/agent-roles.md)
- [Memory System](references/memory-system.md)
- [Approval Workflow](references/approval-workflow.md)
- [Signals Protocol](references/signals-protocol.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell commands, JavaScript setup scripts, JSON configuration, and workspace file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates OpenClaw workspace files, agent configuration, cron job definitions, Telegram topic routing, and brand knowledge templates during setup.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
