## Description:

Gowok is a Go library skill that guides developers using Gowok utilities for project bootstrapping, configuration, HTTP routing, runners, singleton containers, nil-safe values, and SQL connections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hadihammurabi](https://clawhub.ai/user/hadihammurabi)

### License/Terms of Use:


## Use Case:

Developers use this skill for guidance on starting Go projects with Gowok, configuring services, routing HTTP requests, managing runners and singletons, and wiring SQL connections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration examples may expose secrets if copied into application logs or diagnostics.

Mitigation: Avoid logging full gowok.Config or gowok.Config.Map(); redact sensitive values and store production secrets in environment variables or a secret manager.

## Reference(s):

- [Gowok Skill Page](https://clawhub.ai/hadihammurabi/skills/gowok)
- [Getting Started](references/getting-started.md)
- [Configuration](references/configuration.md)
- [Runner](references/runner.md)
- [Singleton](references/singleton.md)
- [Some (Nil Safety)](references/some.md)
- [SQL](references/sql.md)
- [Web](references/web.md)
- [Gowok Releases](https://github.com/gowok/gowok/releases)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Go, YAML, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
