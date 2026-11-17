## Description:

Writes, debugs, and reviews Go code, including goroutine leaks, data races, nil interfaces, slices and maps, Go modules, net/http, testing, performance, deployment, and security guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill for Go implementation, debugging, review, testing, performance tuning, dependency work, and deployment guidance. It is most relevant when diagnosing Go panics, races, hangs, leaks, module conflicts, HTTP behavior, or version-specific language and toolchain issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Suggested commands may update dependencies, build containers, or modify go.mod and go.sum.

Mitigation: Review commands before execution and inspect repository changes after running dependency, build, or module-management commands.

Risk: Stated Go preferences may be stored under ~/Clawic/data/go/config.yaml.

Mitigation: Review stored preferences periodically and avoid saving secrets or project-sensitive values in skill preference data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/go)
- [Clawic Go Skill Page](https://clawic.com/skills/go)
- [Publisher Profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, plain text guidance, Go code snippets, shell commands, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May tailor recommendations to stored Go preferences such as minimum Go version, package layout, test style, HTTP stack, logger, cgo posture, target platform, and timeout defaults.]

## Skill Version(s):

1.0.4 (source: frontmatter and server evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
