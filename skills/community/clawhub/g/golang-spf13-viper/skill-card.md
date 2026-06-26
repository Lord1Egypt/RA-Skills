## Description: <br>
Guides AI coding agents and Go developers through spf13/viper configuration patterns, including layered precedence, flag and environment binding, config files, unmarshalling, hot reload, test isolation, and remote key-value configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill when adding, debugging, or reviewing spf13/viper configuration in Go projects. It helps agents propose code and guidance for precedence rules, flags, environment variables, config files, struct unmarshalling, hot reload, and test isolation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated changes may alter configuration precedence, environment-variable bindings, dependency versions, remote configuration endpoints, or git state. <br>
Mitigation: Review generated code changes before applying them, with extra attention to dependency updates, credential-bearing config keys, remote providers, and git operations. <br>
Risk: Misconfigured viper usage can cause hidden runtime behavior, such as environment variables shadowing files or tests sharing global viper state. <br>
Mitigation: Follow the skill's documented patterns for explicit binding, mapstructure tags, graceful config-file handling, per-test viper instances, and hot-reload testing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/samber/golang-spf13-viper) <br>
- [Publisher profile](https://clawhub.ai/user/samber) <br>
- [Skill homepage](https://github.com/samber/cc-skills-golang) <br>
- [spf13/viper package documentation](https://pkg.go.dev/github.com/spf13/viper) <br>
- [spf13/viper repository](https://github.com/spf13/viper) <br>
- [Viper Env Binding and Flag Binding](references/binding-and-env.md) <br>
- [Viper Config Sources and File Formats](references/sources-and-formats.md) <br>
- [Viper Test Isolation](references/testing-and-isolation.md) <br>
- [Viper Unmarshal Patterns](references/unmarshal.md) <br>
- [Viper Watch and Reload](references/watch-and-reload.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Go code examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include concrete Go snippets, configuration advice, dependency commands, and review guidance for generated changes.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
