## Description:

Provides production-ready autonomous agent operations with cost optimization, task autonomy, persistent memory, security, and scheduled execution workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erich1566](https://clawhub.ai/user/erich1566)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill pack to configure OpenClaw agents for autonomous operations, including model routing, task continuity, progress logging, persistent memory, testing discipline, and scheduled cron-based work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unattended scheduled agent work can continue tasks without timely human review.

Mitigation: Start cron usage with dry runs, restrict writable directories and external integrations, and require approval for dependency installs, deployments, destructive commands, credentials, and production changes.

Risk: Persistent memory and progress logs can capture sensitive information if users store secrets or private raw logs there.

Mitigation: Keep USER.md, MEMORY.md, STATE.md, Todo.md, and progress-log.md free of secrets and private raw logs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/erich1566/skills/openclaw-ops-skills)
- [README](artifact/README.md)
- [Quick Start Guide](artifact/QUICKSTART.md)
- [Feature Guide](artifact/FEATURES.md)
- [Cron Orchestration](artifact/skills/cron-orchestration.md)
- [Security Hardening](artifact/skills/security-hardening.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with configuration snippets and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes workspace templates, installation steps, model routing guidance, cron setup examples, and operational checklists.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
