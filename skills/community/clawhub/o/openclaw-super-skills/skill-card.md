## Description:

Decomposes complex user requests into executable subtasks, identifies required capabilities, searches for existing skills at skills.sh, and creates new skills when no solution exists.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpzhengcn](https://clawhub.ai/user/jpzhengcn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to break complex, multi-step requests into subtasks, map those subtasks to capability types, search for existing skills, and draft plans for creating missing skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill recommends installing third-party skills globally with unpinned, auto-confirmed commands.

Mitigation: Review discovered or generated skills before activation, avoid the documented -g -y pattern, prefer pinned tool and skill versions, and use a local or sandboxed installation scope where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpzhengcn/skills/openclaw-super-skills)
- [Universal Capability Types Reference](references/capability_types.md)
- [skills.sh](https://skills.sh/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with structured task lists, YAML examples, tables, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include skill search recommendations, generated skill templates, execution plans, and verification steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
