## Description:

Deploy a production-ready multi-agent OpenClaw fleet with workspace scaffolding, routing, memory sync, and VPS deployment patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abhinas90](https://clawhub.ai/user/abhinas90)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to scaffold, configure, synchronize, and deploy a small OpenClaw multi-agent fleet on VPS-hosted infrastructure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The deployment script can make broad remote changes and restart the OpenClaw container.

Mitigation: Review and harden deploy.sh before use, avoid root SSH where possible, and use a dedicated deployment account.

Risk: The memory synchronization script can persist and propagate Cross-Agent Intel across multiple agent workspaces.

Mitigation: Run memory_sync.py manually or only after trust review, back up MEMORY.md files first, and treat synchronized intel as untrusted reference data.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python, shell, and JSON configuration artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces workspace scaffolding, OpenClaw routing configuration, memory synchronization updates, and deployment commands that should be reviewed before execution.]

## Skill Version(s):

1.0.2 (source: server release evidence and artifact/skill.json; artifact/SKILL.md frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
