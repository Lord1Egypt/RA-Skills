## Description:

Provides a guide for setting up Golang project layouts and workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose and create Go project layouts for CLIs, libraries, services, monorepos, and workspaces while applying module naming, testing, configuration, and internal/pkg conventions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may direct an agent to modify persistent agent instruction files so another skill is always loaded in future sessions.

Mitigation: Do not allow edits to CLAUDE.md, AGENTS.md, or similar files unless that exact change was explicitly requested and the referenced external skill has been reviewed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samber/skills/golang-project-layout)
- [Project Homepage](https://github.com/samber/cc-skills-golang)
- [12-Factor App](https://12factor.net/)
- [Application Configuration with Cobra + Viper](references/config.md)
- [Directory Layouts](references/directory-layouts.md)
- [Tests, Benchmarks, and Examples](references/testing-layout.md)
- [Go Workspaces for Multi-Package Repositories](references/workspaces.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with Go directory trees, code snippets, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May ask architecture and dependency-injection questions before proposing structure.]

## Skill Version(s):

1.4.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
