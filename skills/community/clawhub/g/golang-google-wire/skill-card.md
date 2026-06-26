## Description: <br>
Helps coding agents use google/wire for compile-time dependency injection in Go projects, including provider sets, injectors, interface bindings, generated wire_gen.go files, cleanup functions, testing patterns, and related Wire commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to adopt or maintain google/wire dependency injection in Go codebases, generate and check injector output, and avoid common compile-time graph and build-tag mistakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may install or run the wire CLI and Go-related commands in a project workspace. <br>
Mitigation: Use it only in intended Go repositories, review proposed shell commands before execution, and confirm tool installation sources match project policy. <br>
Risk: The skill may modify Go source files and generated wire_gen.go files. <br>
Mitigation: Review generated diffs before committing and run the project test or build workflow after Wire regeneration. <br>
Risk: Dependency-injection changes can alter application initialization, cleanup behavior, or provider selection. <br>
Mitigation: Check provider graph changes carefully, rerun wire ./... or wire check ./..., and validate affected startup and integration paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samber/golang-google-wire) <br>
- [Publisher profile](https://clawhub.ai/user/samber) <br>
- [Skill homepage](https://github.com/samber/cc-skills-golang) <br>
- [pkg.go.dev google/wire](https://pkg.go.dev/github.com/google/wire) <br>
- [google/wire repository](https://github.com/google/wire) <br>
- [google/wire user guide](https://github.com/google/wire/blob/main/docs/guide.md) <br>
- [google/wire best practices](https://github.com/google/wire/blob/main/docs/best-practices.md) <br>
- [Advanced google/wire reference](references/advanced.md) <br>
- [google/wire recipes](references/recipes.md) <br>
- [google/wire testing reference](references/testing.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown with Go and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose edits to Go source, injector files, generated wire_gen.go files, and Go or Wire command invocations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
