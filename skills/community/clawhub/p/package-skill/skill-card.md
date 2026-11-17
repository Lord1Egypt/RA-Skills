## Description:

Create and manage skill packages, which bundle related skills into a single top-level skill with internal dispatch.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aiguozhi123456](https://clawhub.ai/user/aiguozhi123456)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and skill-library maintainers use this skill to consolidate related skills, reduce top-level skill count, refresh package registries, and restore packaged sub-skills when needed.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Package create and add operations remove original top-level skill directories after copying them into a package.

Mitigation: Back up the skills folder and review the selected package and skill names before running create or add commands.

Risk: Remove operations move packaged sub-skills back to the top-level skills directory and can change the active skill inventory.

Mitigation: Confirm the destination does not already contain the restored skill and inspect the resulting skill layout before reuse.

Risk: Generated package SKILL.md and pack.md files become persistent agent instructions and may include descriptions from packaged third-party skills.

Mitigation: Inspect generated package files and packaged sub-skill instructions before enabling or distributing the package.

Risk: The security verdict is suspicious because the skill can move or delete installed skills and lacks enough safeguards.

Mitigation: Use only on trusted skill directories, check source skill directories for symlinks, and follow the release security guidance before installation.

## Reference(s):

- [ClawHub Package Skill listing](https://clawhub.ai/aiguozhi123456/skills/package-skill)
- [ClawHub publisher profile](https://clawhub.ai/user/aiguozhi123456)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with command examples and generated skill package files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update package SKILL.md and pack.md files and move skill directories as part of package management.]

## Skill Version(s):

1.0.2 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
