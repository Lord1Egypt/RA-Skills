## Description:

Exports and imports OpenClaw agent configuration as a shareable Markdown ability package, with selective import and privacy reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aitowerofbabel-lang](https://clawhub.ai/user/aitowerofbabel-lang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to back up, share, or import OpenClaw configuration files such as AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, and MEMORY.md after previewing selected content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Imported ability packages can overwrite persistent agent configuration and memory files.

Mitigation: Preview every section, import only the selected files, and keep backups of AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, and MEMORY.md before writing changes.

Risk: MEMORY.md and IDENTITY.md may contain personal preferences, identity details, or other persistent state.

Mitigation: Avoid exporting or importing MEMORY.md or IDENTITY.md unless the user explicitly confirms they are comfortable sharing or replacing that state.

Risk: Ability packages from untrusted sources can alter future agent behavior.

Mitigation: Use packages only from trusted sources and prefer a pinned or otherwise verified install source before import.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aitowerofbabel-lang/skills/openclaw-ability-export)
- [Skill homepage](https://clawic.com/skills/openclaw-ability-export)
- [ClawHub browse page](https://clawhub.com/skills/openclaw-ability-export)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Configuration, Guidance]

**Output Format:** [Markdown ability packages and concise chat responses; selected imports write workspace configuration files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May overwrite selected AGENTS.md, SOUL.md, TOOLS.md, IDENTITY.md, and MEMORY.md files in the workspace root.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact frontmatter is 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
