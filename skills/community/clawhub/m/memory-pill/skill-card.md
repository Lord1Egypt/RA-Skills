## Description:

Memory Pill is an AI-native memory and orchestration system for OpenClaw that helps agents use persistent memory, behavioral scaffolding, and delegation patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[7d-codes](https://clawhub.ai/user/7d-codes)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to add persistent workspace memory, agent behavior files, project summaries, daily notes, and orchestration guidance to an OpenClaw environment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and behavior files can change how future OpenClaw sessions operate.

Mitigation: Install only when a global persistent memory system is intended, and require separate confirmation plus a diff before each modification.

Risk: Stored user context may include sensitive personal details or secrets.

Mitigation: Avoid storing secrets or sensitive personal details, and review the exact files the skill may read or write before activation.

Risk: Existing SOUL.md, AGENTS.md, USER.md, and memory files may be overwritten or altered during setup.

Mitigation: Keep backups of existing memory and behavior files before using the skill.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON/YAML file templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose or create persistent OpenClaw workspace files after user confirmation.]

## Skill Version(s):

0.8.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
