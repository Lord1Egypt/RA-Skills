## Description:

帮我写个 skill。

This skill is ready for commercial/non-commercial use.

## Publisher:

[54lynnn](https://clawhub.ai/user/54lynnn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to create focused OpenClaw skills, choose an appropriate file structure, write usable SKILL.md instructions, and add scripts, references, examples, or evals when they are justified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional evaluator install command could introduce an unreviewed dependency if the package source is not checked.

Mitigation: Verify the eval-skill package source and prefer a pinned or reviewed version before running the install command.

Risk: Overly broad generated skill descriptions can cause agents to trigger the skill in the wrong situations.

Mitigation: Review generated descriptions and make them specific to the intended user request and task boundary.

## Reference(s):

- [SKILL.md](artifact/SKILL.md)
- [SKILL.md template](artifact/references/skill-template.md)
- [ClawHub skill page](https://clawhub.ai/54lynnn/skills/meta-skill-writer)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with YAML frontmatter, directory layouts, code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce skill file content, directory recommendations, self-checklists, and optional evaluator installation guidance.]

## Skill Version(s):

1.3.1 (source: release metadata; artifact frontmatter says 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
