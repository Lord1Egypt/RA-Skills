## Description:

Local Skill Manager helps an agent list installed skills, inspect skill versions, scaffold new local skills, and remove local skill directories with deletion guardrails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenchen913](https://clawhub.ai/user/chenchen913)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to manage local skill folders: enumerate installed skills, check version metadata, create a standard skill scaffold, and remove skills when they are no longer needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can delete local skill directories when asked to remove a skill.

Mitigation: Use the documented --dry-run mode before deletion, review the target path, and avoid --force unless the deletion is intentional.

Risk: The skill depends on PyYAML without a pinned version.

Mitigation: Pin PyYAML in controlled environments when reproducible installs or dependency review are required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenchen913/skills/local-skill-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and generated local skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read local SKILL.md metadata, create scaffold directories and files, or delete a selected skill directory through the bundled scripts.]

## Skill Version(s):

1.0.1 (source: release evidence; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
