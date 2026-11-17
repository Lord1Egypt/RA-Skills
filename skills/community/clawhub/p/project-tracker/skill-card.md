## Description:

Multi-project tracker with status dashboards, milestone tracking, stalled project detection, priority scoring, and automated weekly progress reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clawdssen](https://clawhub.ai/user/clawdssen)

### License/Terms of Use:

CC-BY-NC-4.0

## Use Case:

External users use this skill to have an agent maintain Markdown project dashboards, milestone logs, stalled-project flags, priority scores, weekly reviews, and status updates across multiple projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create or update local Markdown project records, which may add noisy or unintended files or capture sensitive business details if prompts are broad.

Mitigation: Use explicit requests for specific project entries or dashboard updates, review generated records before relying on them, and avoid storing sensitive business details unless appropriate.

## Reference(s):

- [Project Tracker on ClawHub](https://clawhub.ai/clawdssen/skills/project-tracker)
- [Project Tracker Advanced Patterns](artifact/references/advanced-patterns.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance]

**Output Format:** [Markdown project records, dashboards, weekly reviews, priority-scoring tables, and status updates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local project-tracking files when requested]

## Skill Version(s):

1.0.0 (source: server-resolved release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
