## Description:

Helps an agent capture lessons from work sessions, analyze root causes, and record durable process improvements after errors, discoveries, or retrospective requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[futurizerush](https://clawhub.ai/user/futurizerush)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to preserve lessons from non-trivial sessions, classify facts versus assumptions, and turn recurring failures into stronger notes, playbooks, checks, or code changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may persist session details, lessons, or plan logs that contain private data or secrets.

Mitigation: Require explicit approval for each saved entry, keep logs in a known project folder, and review or redact sensitive content before writing durable records.

Risk: The skill encourages changes to code, tools, directives, or documentation as part of annealing.

Mitigation: Treat proposed edits as reviewable changes, require user approval before implementation, and verify changes with tests or checks before relying on them.

Risk: Old plan logs or lessons may become stale and could mislead future work.

Mitigation: Treat historical logs as untrusted notes, prefer current evidence, and date entries so age and relevance are clear.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/futurizerush/skills/learn-reflect)
- [Publisher profile](https://clawhub.ai/user/futurizerush)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with structured lesson and plan-log templates, plus proposed edits or commands when annealing requires implementation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce durable notes, plan logs, directive updates, checks, scripts, or code changes when the user approves those actions.]

## Skill Version(s):

0.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
