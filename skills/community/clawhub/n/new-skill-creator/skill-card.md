## Description:

Creates new agent skills from scratch through guided requirements gathering, skill-directory scaffolding, and SKILL.md authoring support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fwwdn](https://clawhub.ai/user/fwwdn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent-skill authors use this skill to turn a skill idea into a publishable package with frontmatter, workflow instructions, examples, metadata, and supporting references. It can scaffold instruction-only, script-backed, or asset-backed skill directories with a bundled Python script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scaffold script creates files in a user-selected output directory.

Mitigation: Confirm the destination path before running the scaffold command and avoid targeting directories that already contain unrelated work.

Risk: Generated skill templates contain TODO placeholders and draft guidance that may be incomplete.

Mitigation: Review and replace placeholders, then run quality and security checks before publishing or relying on the generated skill.

## Reference(s):

- [Skill Anatomy](references/skill-anatomy.md)
- [Writing Guide](references/writing-guide.md)
- [Examples](references/examples.md)
- [ClawHub Skill Page](https://clawhub.ai/fwwdn/skills/new-skill-creator)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell commands and generated skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 when using the scaffold script.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
