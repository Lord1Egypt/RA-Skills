## Description:

InspirAI Skill Audit helps agents scan installed skills and commands for functional overlap, inspect audit status, and guide resolution of redundant entries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexxxiong](https://clawhub.ai/user/alexxxiong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users managing ClawHub or Claude skill setups use this skill to identify overlapping commands and skills, review audit status, and decide which redundant entries to keep or disable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The resolve workflow can change installed command or plugin state.

Mitigation: Use scan and status as inventory aids, run resolve with dry-run first, and back up ~/.claude/commands and ~/.claude/plugins/installed_plugins.json before permitting disable actions.

Risk: The artifact contains contradictory plugin-disabling guidance, including unsafe direct registry edits.

Mitigation: Avoid direct plugin registry edits and prefer supported plugin commands or manual review before changing installed plugin state.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/alexxxiong/skills/inspirai-audit)
- [Publisher profile](https://clawhub.ai/user/alexxxiong)
- [Skill definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown reports, status summaries, interactive decision prompts, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce configuration-changing guidance during resolve flows; dry-run and backup review are recommended before disabling anything.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
