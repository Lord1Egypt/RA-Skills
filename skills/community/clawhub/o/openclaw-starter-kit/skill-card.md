## Description:

OpenClaw Starter Kit interactively guides Korean-language OpenClaw beginners through initial setup, starter memory and heartbeat files, recommended skills, cron basics, troubleshooting, and security hardening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gyeuun97](https://clawhub.ai/user/gyeuun97)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and developers use this skill to bootstrap a Korean-language OpenClaw workspace, create starter persona, user, memory, heartbeat, and agent files, configure search and recommended skills, and review basic operational security.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Troubleshooting guidance includes a root-level npm install command.

Mitigation: Prefer a user-scoped install method, verify package provenance, and avoid running the sudo install command unless it is explicitly required and reviewed.

Risk: Cron jobs and HEARTBEAT.md tasks can create persistent automation that acts on a schedule.

Mitigation: Enable only intentional schedules and tasks, review their permissions, and require approval for external messages, deletion, purchases, or other consequential actions.

Risk: Recommended skills and force reinstalls can expand tool access unexpectedly.

Mitigation: Install only the exact skills needed, review each skill before use, and avoid force reinstalls unless recovering a known broken installation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/gyeuun97/skills/openclaw-starter-kit)
- [OpenClaw security guide](guides/security-guide.md)
- [OpenClaw skill recommendations guide](guides/skill-recommendations.md)
- [OpenClaw cron basics guide](guides/cron-basics.md)
- [OpenClaw troubleshooting guide](guides/troubleshooting.md)
- [Brave Search API](https://brave.com/search/api/)
- [OpenClaw Discord community](https://discord.com/invite/clawd)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent in creating starter files such as SOUL.md, USER.md, MEMORY.md, HEARTBEAT.md, and AGENTS.md from bundled templates.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
