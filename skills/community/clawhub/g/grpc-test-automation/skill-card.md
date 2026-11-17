## Description:

Complete gRPC test automation for embedded devices with C/C++ SDKs, producing a test framework, JMeter JMX plans, and Excel reports from requirements and SDK inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ventus-z](https://clawhub.ai/user/ventus-z)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and test engineers use this skill to build a lab workflow for testing C/C++ SDK interfaces on embedded boards through generated gRPC services, JMeter test plans, serial-style deployment flows, and Excel result reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence flags unauthenticated network services and under-scoped board deployment patterns.

Mitigation: Use the skill in an isolated lab environment and review, harden, and restrict generated services before exposing them beyond that environment.

Risk: The release evidence flags automatic package installation in included scripts.

Mitigation: Review dependency installation behavior before running scripts, and avoid privileged or shared execution environments.

Risk: The release evidence advises validating project paths and treating generated reports as untrusted test data.

Mitigation: Validate project paths and deployment targets before execution, and handle generated Excel reports as untrusted files when opening or sharing them.

## Reference(s):

- [SDK Header Analysis Guide](references/sdk-analysis.md)
- [C++ gRPC Server Implementation Guide](references/cpp-server.md)
- [Proto Design Guide](references/proto-design.md)
- [JMeter gRPC Plugin Configuration](references/jmeter-config.md)
- [JMX Template Guide](references/jmx-template.md)
- [Serial Communication Protocol](references/serial-protocol.md)
- [Test Case Patterns](references/test-patterns.md)
- [Excel Report Format](references/excel-format.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, files]

**Output Format:** [Markdown guidance with generated project files, proto definitions, JMX XML, shell commands, and Excel report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local test framework artifacts that should be reviewed before lab execution.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
