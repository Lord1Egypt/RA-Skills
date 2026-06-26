## Description: <br>
Go application architecture with net/http 1.22+ routing, project structure patterns, graceful shutdown, and dependency injection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to design, scaffold, and review Go web services that use standard-library routing, explicit dependency wiring, production shutdown handling, and maintainable project layout. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can generate API-routing and API-hardening guidance that may be incorrect for a specific production service. <br>
Mitigation: Review generated code and recommendations before applying them to production. <br>
Risk: Example handlers and configuration patterns may involve sensitive credentials or API keys. <br>
Mitigation: Keep credentials loaded through explicit configuration or dependency injection, and avoid reading secrets directly inside handlers. <br>


## Reference(s): <br>
- [Go Project Structure](references/project-structure.md) <br>
- [Graceful Shutdown](references/graceful-shutdown.md) <br>
- [Dependency Injection in Go](references/dependency-injection.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with Go code examples, review criteria, and occasional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pass/fail review findings for Go version, composition root, graceful shutdown, and dependency injection patterns.] <br>

## Skill Version(s): <br>
2.3.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
