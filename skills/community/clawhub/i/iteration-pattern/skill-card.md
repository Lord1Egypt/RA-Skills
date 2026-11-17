## Description:

Guides an agent through a Ralph-loop style iteration pattern for complex tasks by defining measurable completion criteria, validating each round, improving failures, and reporting final status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudyli](https://clawhub.ai/user/cloudyli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, and agents use this skill to structure complex work into bounded iterations with explicit deliverables, measurable criteria, validation methods, improvement rounds, and a final completion report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes example validation commands that may inspect local project files or local skill listings if executed by an agent.

Mitigation: Review suggested commands before running them and limit execution to the intended workspace.

Risk: Iteration checklists can still produce incomplete or misleading completion reports if the initial criteria are vague.

Mitigation: Require concrete deliverables, measurable quality standards, and explicit validation methods before starting an iteration.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cloudyli/skills/iteration-pattern)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown checklists, workflow steps, tables, prompt templates, and optional validation command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow guidance; no executable code is included in the artifact.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter is 1.0.0 and artifact _meta.json is 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
