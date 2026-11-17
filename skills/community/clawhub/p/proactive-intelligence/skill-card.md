## Description:

Proactive Intelligence helps agents anticipate user needs, maintain local memory, learn from corrections, manage skills, and propose or apply skill improvements.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cle87937-code](https://clawhub.ai/user/cle87937-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to make an assistant more proactive and self-improving through local memory, structured learning logs, and skill management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently change agent memory, workspace Markdown files, and other installed skills with too little scoping or user control.

Mitigation: Review the scripts before installation, back up workspace Markdown files and installed skills, and avoid running the initializer or skill-evolver in important workspaces unless persistent memory and cross-skill changes are acceptable.

Risk: Generated memory and .learnings files are long-lived local records that may influence future agent behavior.

Mitigation: Periodically review these files and remove stale, sensitive, or inaccurate records before relying on the skill in ongoing work.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cle87937-code/skills/proactive-intelligence)
- [Setup guide](artifact/setup.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration paths, and optional JSON reports or local files created by scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent local memory files, structured learning logs, skill backups, and skill health reports when its scripts are run.]

## Skill Version(s):

2.3.1 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
