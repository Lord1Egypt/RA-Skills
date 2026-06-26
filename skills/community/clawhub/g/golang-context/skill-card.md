## Description: <br>
Guides AI coding agents on idiomatic Go context.Context usage, including propagation, cancellation, timeouts, deadlines, request-scoped values, and context.WithoutCancel for background work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI coding agents use this skill when designing or reviewing Go code that must propagate context across HTTP handlers, services, databases, external calls, goroutines, and tracing boundaries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release has broad coding-tool permissions and server capability tags that appear unrelated to the documentation-only skill content. <br>
Mitigation: Review permissions and displayed capability tags before deployment; rely on the documented Go context guidance rather than the unrelated tags. <br>


## Reference(s): <br>
- [Cancellation, Timeouts & Deadlines](references/cancellation.md) <br>
- [Context in HTTP Servers & Service Calls](references/http-services.md) <br>
- [Context Values & Cross-Service Tracing](references/values-tracing.md) <br>
- [Project homepage](https://github.com/samber/cc-skills-golang) <br>
- [ClawHub skill page](https://clawhub.ai/samber/golang-context) <br>
- [Publisher profile](https://clawhub.ai/user/samber) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Go code examples and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; requires the Go toolchain when commands are used.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
