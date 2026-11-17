## Description:

Migrates a Number Two OpenClaw agent state by restoring identity, memory, skill integrations, system configuration, environment setup, and verification assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fr33b1rd8979-max](https://clawhub.ai/user/fr33b1rd8979-max)

### License/Terms of Use:

MIT

## Use Case:

OpenClaw users and agent operators use this skill to move a specific agent workspace state to a new environment, including identity, memory, skills, current project state, and validation steps. It is intended for deliberate workspace restoration, not general-purpose OpenClaw setup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill replaces active OpenClaw workspace identity, memory, rules, skills, and state with a specific agent state.

Mitigation: Install only when that replacement is intended; review identity, AGENTS, SOUL, memory, and skills files before installation and use a separate test profile or complete backup.

Risk: Bundled plaintext credentials or copied environment variables may be exposed, stale, or inappropriate for the target environment.

Mitigation: Remove bundled secrets before use, rotate any exposed keys, and configure fresh credentials through the target environment's normal secret-management process.

Risk: Restored identity, rule, and memory files can materially change the agent's behavior after installation.

Mitigation: Validate behavior in an isolated workspace before using the migrated state for ongoing work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fr33b1rd8979-max/skills/number-two-migration)
- [SKILL.md](artifact/SKILL.md)
- [README.md](artifact/README.md)
- [Number Two Full State Migration Guide](artifact/二号完整状态迁移指南.md)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell scripts and JSON/Markdown configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Install flow can overwrite an OpenClaw workspace and write environment variables after user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
