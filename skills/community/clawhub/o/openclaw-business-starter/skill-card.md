## Description:

Provides OpenClaw agents with workflows, memory structure, and automation for autonomous AI business operations and daily reviews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tara-quinn-ai](https://clawhub.ai/user/tara-quinn-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to bootstrap an autonomous business-agent workspace with PARA memory folders, daily review prompts, heartbeat guidance, and scheduled memory consolidation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup script can overwrite core workspace identity, policy, heartbeat, tool, and memory files.

Mitigation: Install only into a fresh or backed-up OpenClaw workspace and review the generated files before restarting the gateway.

Risk: The bundled operating templates contain hardcoded Tara/Kalin-specific command identities and authority assumptions.

Mitigation: Replace the user, bot, and authenticated-channel rules in AGENTS.md, SOUL.md, USER.md, and related templates before enabling the agent.

Risk: The skill creates scheduled morning review and nightly memory consolidation jobs that write to workspace memory.

Mitigation: Disable or edit the cron jobs if automatic briefings, memory consolidation, or QMD indexing are not desired.

## Reference(s):

- [OpenClaw Documentation](https://docs.openclaw.ai)
- [ClawHub Skill Page](https://clawhub.ai/tara-quinn-ai/skills/openclaw-business-starter)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, setup shell commands, workspace template files, and scheduled job instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Installs and updates local OpenClaw workspace files and cron jobs when the setup script is run.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
