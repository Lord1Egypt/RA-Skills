## Description: <br>
Structured error handling in Golang with samber/oops, covering error builders, stack traces, error codes, error context, wrapping, attributes, user-facing messages, panic recovery, and logger integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when adopting or maintaining samber/oops in Go services. It helps agents generate and review structured error handling patterns for wrapping errors, propagating context, separating public and technical messages, recovering panics, and integrating logs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated error-handling examples may attach sensitive user, request, response, query, credential, or raw input data to errors that flow into logs or observability systems. <br>
Mitigation: Keep request and response bodies disabled by default, avoid emails, tokens, cookies, authorization headers, credentials, and raw user input in error attributes, and use allowlisted, redacted, truncated, or hashed fields for observability exports. <br>


## Reference(s): <br>
- [Skill homepage](https://github.com/samber/cc-skills-golang) <br>
- [samber/oops repository](https://github.com/samber/oops) <br>
- [samber/oops Go package documentation](https://pkg.go.dev/github.com/samber/oops) <br>
- [Advanced patterns](references/advanced.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Go code examples and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May rely on the Go toolchain and samber/oops documentation for validation and examples.] <br>

## Skill Version(s): <br>
1.1.3 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
