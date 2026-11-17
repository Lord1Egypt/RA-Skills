## Description:

Architecture guide for running multiple specialized AI agents on a single OpenClaw server, covering workspace isolation, agent roles, shared memory, Telegram routing, rate limit management, monitoring, and self-healing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mosoonpi-ai](https://clawhub.ai/user/mosoonpi-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan and run multiple specialized OpenClaw agents on one server with isolated workspaces, role-specific configuration, Telegram routing, shared memory, monitoring, and backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Cron jobs, backup automation, shared memory, and symlinked skills can affect running services or expose data across agents if applied too broadly.

Mitigation: Apply automation only to intended workspaces, review shared paths before deployment, and scope shared memory and symlinks to utilities that are safe for multiple agents.

Risk: Bot and API tokens used for Telegram routing and multi-token rate-limit management can expose agent access if mishandled.

Mitigation: Protect tokens, avoid storing them in git or chat logs, and configure allowed chat IDs for all bots.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mosoonpi-ai/skills/multi-agent-architecture)
- [README](artifact/README.md)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Documentation-only skill that provides architecture patterns, setup steps, operational checklists, and example commands.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
