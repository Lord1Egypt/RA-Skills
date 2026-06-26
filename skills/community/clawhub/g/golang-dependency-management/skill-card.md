## Description: <br>
Dependency management strategies for Golang projects, including go.mod management, package installation and upgrades, Minimal Version Selection, vulnerability scanning, outdated dependency tracking, binary size analysis, automated dependency updates, conflict resolution, and go.work workspaces. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to manage Go module dependencies, evaluate new packages, upgrade or remove modules, audit vulnerabilities, analyze dependency size, configure update automation, and resolve module or workspace conflicts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may modify dependency, workspace, or CI configuration files and may run Go or git commands. <br>
Mitigation: Review proposed go.mod, go.sum, go.work, and CI changes before committing them. <br>
Risk: Adding unnecessary or low-quality dependencies can increase maintenance burden and supply-chain exposure. <br>
Mitigation: Require confirmation before adding new dependencies, check standard-library alternatives, review package quality and license compatibility, and run govulncheck for release workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samber/golang-dependency-management) <br>
- [Project homepage](https://github.com/samber/cc-skills-golang) <br>
- [Versioning and Minimal Version Selection](references/versioning.md) <br>
- [Auditing Dependencies](references/auditing.md) <br>
- [Dependency Conflicts and Resolution](references/conflicts.md) <br>
- [Go Workspaces](references/workspaces.md) <br>
- [Automated Dependency Updates](references/automated-updates.md) <br>
- [Visualizing the Dependency Graph](references/visualization.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code and shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to Go module, workspace, and dependency-update configuration files; user review is expected before committing changes.] <br>

## Skill Version(s): <br>
1.2.3 (source: release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
