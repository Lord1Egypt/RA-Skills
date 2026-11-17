## Description:

Generates phased, dependency-ordered tasks from a specification. Use after the spec, before implementation

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill after completing a specification to create phased implementation tasks with explicit dependencies, parallel work opportunities, affected files, and completion criteria.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because a local path-like reference in SKILL.md did not match a bundled artifact, leaving coverage incomplete.

Mitigation: Review the unresolved reference and scan the complete release artifacts before execution.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/athola/skills/nm-spec-kit-task-planning)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/spec-kit)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown task plan organized into phases, with task IDs, dependencies, parallel markers, affected files, and completion criteria.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dependency-ordered implementation tasks; parallel work is marked only when the stated nonconflict criteria are met.]

## Skill Version(s):

1.10.3 (source: SKILL.md frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
