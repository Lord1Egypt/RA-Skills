## Description: <br>
Modernizes Go codebases with recent language features, standard library improvements, tooling updates, and idiomatic patterns while respecting project Go version constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to review, modernize, and maintain Go projects across Go 1.21 through Go 1.26. It helps identify version-appropriate language, standard library, testing, security, dependency, and CI/tooling improvements. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Modernization changes may affect go.mod, go.sum, CI/tooling files, dependencies, or .modernize entries. <br>
Mitigation: Review diffs before accepting edits and run go mod tidy, tests, and relevant linters before merging. <br>
Risk: Dependency updates or tooling migrations may introduce compatibility or workflow changes. <br>
Mitigation: Check changelogs and release notes for breaking changes before proceeding with dependency or tool upgrades. <br>
Risk: Contextual modernization suggestions can distract from an unrelated active coding task. <br>
Mitigation: For non-explicit triggers, ask for consent once and stop suggesting modernization if the user declines. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/samber/golang-modernize) <br>
- [Publisher Profile](https://clawhub.ai/user/samber) <br>
- [Project Homepage](https://github.com/samber/cc-skills-golang) <br>
- [Go Version Modernizations](references/versions.md) <br>
- [Tooling Modernization](references/tooling.md) <br>
- [Go 1.21 Release Notes](https://go.dev/doc/go1.21) <br>
- [Go 1.22 Release Notes](https://go.dev/doc/go1.22) <br>
- [Go 1.23 Release Notes](https://go.dev/doc/go1.23) <br>
- [Go 1.24 Release Notes](https://go.dev/doc/go1.24) <br>
- [Go 1.25 Release Notes](https://go.dev/doc/go1.25) <br>
- [Go 1.26 Release Notes](https://go.dev/doc/go1.26) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with code snippets, shell commands, configuration suggestions, and optional code edits.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Version-aware recommendations based on the target Go version and project context.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
