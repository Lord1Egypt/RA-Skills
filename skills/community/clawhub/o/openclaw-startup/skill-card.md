## Description:

First-run setup wizard for new OpenClaw agents that interviews the user, generates tailored workspace files, scaffolds memory, recommends operational crons, walks through security baseline setup, and recommends companion skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zurbrick](https://clawhub.ai/user/zurbrick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to bootstrap a new agent workspace, personalize identity and memory files, configure operational routines, and apply baseline safety controls. It is intended for first-run setup, onboarding, or resetting an agent to a clean baseline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer can initialize Git and commit all workspace contents, which may preserve sensitive files in repository history.

Mitigation: Run the installer only in a new or inspected workspace, and avoid or modify the Git initialization and commit behavior unless secrets and private files have been excluded.

Risk: Heartbeat, backup, and companion-skill setup can expand what the agent reads, persists, or runs on a schedule.

Mitigation: Keep those features opt-in, confirm approved data sources and schedules with the user, and review installed crons after setup.

## Reference(s):

- [OpenClaw Startup Skill Page](https://clawhub.ai/zurbrick/skills/openclaw-startup)
- [Interview Guide](references/interview-guide.md)
- [Cron Recipes](references/cron-recipes.md)
- [Security Baseline](references/security-baseline.md)
- [Placeholder Map](references/placeholder-map.md)
- [Cognition companion skill](https://clawhub.com/skills/cognition)
- [Summarize companion skill](https://clawhub.com/skills/summarize)
- [Agent Hardening companion skill](https://clawhub.com/skills/agent-hardening)
- [OpenClaw Backup companion skill](https://clawhub.com/skills/openclaw-backup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, JSON cron examples, and generated workspace file templates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are interactive and should be reviewed with the user before core files, cron schedules, or companion-skill installs are written.]

## Skill Version(s):

1.0.3 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
