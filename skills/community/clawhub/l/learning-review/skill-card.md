## Description:

Learning Review helps an agent turn learning notes into working habits through post-learning reviews, weekly internalization, application checks, archive compression, and knowledge integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mayf3](https://clawhub.ai/user/mayf3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to review learning outputs and convert useful lessons into persistent agent guidance, memory, skill updates, and review reports. It is intended for follow-up review and internalization rather than first-time study of new material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change long-lived agent behavior files, memory, skills, and archived learning notes.

Mitigation: Run it manually or in propose-only mode when possible, and review diffs before accepting changes to AGENTS.md, TOOLS.md, SOUL.md, MEMORY.md, memory/, learning/, references/, or skill files.

Risk: Scheduled review tasks may silently move notes or compress inline guidance into reference files.

Mitigation: Use scheduled execution only in trusted workspaces and inspect archive, compression, and integration reports after each run.

## Reference(s):

- [Learning Review on ClawHub](https://clawhub.ai/mayf3/skills/learning-review)
- [Cron Configuration Templates](references/cron-templates.md)
- [Review Report Templates](references/templates.md)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports and concise file-update guidance with optional shell commands for directory setup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update learning review files, memory files, agent instruction files, and skill documentation when run with write permissions.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
