## Description: <br>
Provides gRPC usage guidelines, protobuf organization, and production-ready patterns for Golang microservices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[samber](https://clawhub.ai/user/samber) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to implement, review, and debug Go gRPC services and clients, including protobuf layout, code generation, interceptors, status-code handling, TLS/mTLS, graceful shutdown, streaming, and tests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can suggest shell commands and code changes that affect Go and protobuf project behavior. <br>
Mitigation: Review generated commands, generated files, and code changes before execution or merge. <br>
Risk: Generated gRPC examples may be adapted into production services where transport security, reflection, deadlines, and status-code handling affect reliability and exposure. <br>
Mitigation: Confirm TLS or mTLS, disable reflection outside development, set deadlines on client calls, and test expected gRPC status codes before deployment. <br>
Risk: Security evidence recommends installation only when the publisher and intended workflows are trusted. <br>
Mitigation: Install from the server-resolved publisher profile and keep use scoped to Go gRPC development and review workflows. <br>


## Reference(s): <br>
- [Protobuf & Code Generation Reference](references/protoc-reference.md) <br>
- [gRPC Testing Reference](references/testing.md) <br>
- [Project homepage](https://github.com/samber/cc-skills-golang) <br>
- [ClawHub skill page](https://clawhub.ai/samber/golang-grpc) <br>
- [Publisher profile](https://clawhub.ai/user/samber) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Go, protobuf, YAML, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands for Go tooling and protobuf generation; generated code and commands should be reviewed before use.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
