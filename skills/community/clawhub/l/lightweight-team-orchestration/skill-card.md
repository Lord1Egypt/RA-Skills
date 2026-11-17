## Description:

Lightweight multi-agent team orchestration. Output structure simplified to two folders: agents/ and projects/.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to define lightweight multi-agent roles, distribute tasks, and preserve versioned deliverables without a complex workflow engine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated role and project files may encode task assumptions or role behavior that is not appropriate for the collaboration.

Mitigation: Review generated agent role files and scoped task assignments before relying on the team output.

Risk: The workflow can become insufficient for complex multi-stage or large-scale coordination.

Mitigation: Use it for small, scoped collaborations and move complex workflows to a more explicit tracking or orchestration system.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/lightweight-team-orchestration)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with file structure examples and task handoff snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local role definitions and versioned project artifacts when followed by an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
