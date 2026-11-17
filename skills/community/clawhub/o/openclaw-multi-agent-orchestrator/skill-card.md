## Description:

OpenClaw Multi Agent Orchestrator helps agents register collaborators, dispatch tasks, balance load, exchange local messages, and inspect coordination status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[williamwg2025](https://clawhub.ai/user/williamwg2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate multiple local agents for task routing, collaboration tracking, message exchange, and status monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task messages and collaboration records are stored locally in JSON files and may contain sensitive user-provided content.

Mitigation: Avoid putting secrets or confidential data in task messages, and review local configuration and message files before sharing or publishing the skill directory.

Risk: The README recommends optional related-skill installation commands that are separate third-party installs.

Mitigation: Review and pin any optional related-skill install commands before running them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/williamwg2025/skills/openclaw-multi-agent-orchestrator)
- [README_EN.md](artifact/README_EN.md)
- [README.md](artifact/README.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Terminal text output and JSON-backed configuration/state files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Python scripts read and write skill configuration files for agent registry, task history, messages, and collaboration records.]

## Skill Version(s):

0.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
