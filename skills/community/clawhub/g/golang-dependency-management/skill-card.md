## Description:

Dependency management strategies for Golang projects, including go.mod management, package installation and upgrades, Minimal Version Selection, vulnerability scanning, outdated dependency tracking, binary size analysis, automated update setup, conflict resolution, and go.work workspaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to manage Go dependencies safely, including adding, removing, upgrading, auditing, and troubleshooting modules. It helps agents choose safer dependency workflows, preserve checksum integrity, and prepare automated update configurations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent to inspect or modify Go dependency files and run Go-related commands.

Mitigation: Review proposed dependency changes before applying them, run go mod tidy, go test ./..., go vet ./..., and govulncheck ./... before release, and require confirmation before adding new dependencies.

Risk: Installing tools with @latest can make dependency audits depend on changing tool versions.

Mitigation: Pin govulncheck and other Go tools in go.mod with tool directives where supported, or otherwise document and review the chosen tool versions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samber/skills/golang-dependency-management)
- [Project Homepage](https://github.com/samber/cc-skills-golang)
- [Versioning & Minimal Version Selection](references/versioning.md)
- [Auditing Dependencies](references/auditing.md)
- [Dependency Conflicts & Resolution](references/conflicts.md)
- [Go Workspaces](references/workspaces.md)
- [Automated Dependency Updates](references/automated-updates.md)
- [Visualizing the Dependency Graph](references/visualization.md)
- [go-size-analyzer](https://github.com/Zxilly/go-size-analyzer)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown guidance with inline bash, Go module, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May suggest edits to Go dependency files and dependency-update configuration; expects user confirmation before adding new dependencies.]

## Skill Version(s):

1.3.0 (source: release evidence and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
