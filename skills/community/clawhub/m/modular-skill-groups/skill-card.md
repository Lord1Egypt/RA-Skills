## Description:

Organize, activate, and switch between named OpenClaw skill groups to keep agent context focused.

This skill is ready for commercial/non-commercial use.

## Publisher:

[di5cip1e](https://clawhub.ai/user/di5cip1e)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep OpenClaw sessions focused by listing, activating, and maintaining named skill groups for different project phases.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Changing the active skill group can affect which skills load in later OpenClaw sessions.

Mitigation: Switch groups only on explicit user request and verify ~/.openclaw/active_skill_group when the active skill set matters.

## Reference(s):

- [SKILL_GROUPS.md](references/SKILL_GROUPS.md)
- [ClawHub Skill Page](https://clawhub.ai/di5cip1e/skills/modular-skill-groups)
- [Publisher Profile](https://clawhub.ai/user/di5cip1e)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update the active OpenClaw skill group setting when the user explicitly requests a group switch.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
