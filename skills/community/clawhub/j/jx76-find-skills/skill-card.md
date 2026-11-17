## Description:

Helps agents discover and recommend installable skills for user tasks, including search and installation guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jx-76](https://clawhub.ai/user/jx-76)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to discover existing skills for a task, present relevant install options, and guide installation through the Skills CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to run mutable unpinned npx commands.

Mitigation: Prefer pinned CLI versions and review the command before execution.

Risk: The skill may encourage broad global installation of third-party skills.

Mitigation: Avoid global non-interactive installation by default, inspect skill source before installation, and install only from trusted maintainers.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jx-76/skills/jx76-find-skills)
- [Skills Directory](https://skills.sh/)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands]

**Output Format:** [Markdown with inline shell commands and links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include skill names, installation commands, and links to skill listings.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
