## Description:

Golang configuration library using spf13/viper - layered precedence (flag > env > file > KV > default), BindPFlag/BindPFlags, SetEnvPrefix + SetEnvKeyReplacer + AutomaticEnv, ReadInConfig + ConfigFileNotFoundError, Unmarshal + mapstructure struct tags, Sub for sub-trees, WatchConfig + OnConfigChange for hot reload, viper.New() for test isolation, and remote KV integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[samber](https://clawhub.ai/user/samber)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill when adopting or maintaining spf13/viper configuration in Go projects. It guides layered configuration, environment and flag binding, config file loading, struct unmarshalling, hot reload, and test isolation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency examples may use @latest, which can produce non-reproducible builds in production.

Mitigation: Pin the spf13/viper dependency version when applying generated commands in production projects.

Risk: Agent-proposed edits to Go configuration code can alter precedence, defaults, reload behavior, or tests.

Mitigation: Review proposed file edits and run the relevant Go tests, linters, and race checks before merging.

Risk: Configuration work can expose sensitive environment-derived values such as credential paths or secret settings.

Mitigation: Avoid printing, committing, or logging sensitive configuration values while applying the skill's guidance.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/samber/skills/golang-spf13-viper)
- [Clawdis Homepage](https://github.com/samber/cc-skills-golang)
- [pkg.go.dev spf13/viper](https://pkg.go.dev/github.com/spf13/viper)
- [spf13/viper GitHub Repository](https://github.com/spf13/viper)
- [Viper Config Sources and File Formats](references/sources-and-formats.md)
- [Viper Env Binding and Flag Binding](references/binding-and-env.md)
- [Viper Unmarshal and Struct Mapping](references/unmarshal.md)
- [Viper WatchConfig and Hot Reload](references/watch-and-reload.md)
- [Viper Test Isolation](references/testing-and-isolation.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Go and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Go code edits and configuration patterns for projects that use github.com/spf13/viper.]

## Skill Version(s):

1.1.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
