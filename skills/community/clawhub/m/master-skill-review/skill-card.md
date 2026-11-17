## Description:

Review an OpenClaw skill for token efficiency, scriptability, and clean action boundaries; back up first, then improve the skill.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kid0114](https://clawhub.ai/user/kid0114)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill maintainers use this skill to review OpenClaw skills for token efficiency, scriptability, clean action boundaries, and safer change workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect and modify other installed skills using high local permissions.

Mitigation: Use it only for trusted local skills and start in a read-only review mode before allowing edits.

Risk: The skill can make changes without sufficiently clear target boundaries.

Mitigation: Require an explicit diff, confirmed target path, backup location, and confirmation that every changed file is inside the intended skill directory before allowing writes.

## Reference(s):

- [Skill Review Checklist](artifact/references/checklist.md)
- [ClawHub Skill Page](https://clawhub.ai/kid0114/skills/master-skill-review)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown review notes with shell commands and proposed file changes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include backup paths, changed-file summaries, review findings, optimization suggestions, and final evidence.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
