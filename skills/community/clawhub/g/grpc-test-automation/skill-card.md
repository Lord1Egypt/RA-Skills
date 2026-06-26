## Description: <br>
Complete gRPC test automation for embedded devices with C/C++ SDKs, producing a test framework, JMeter test plan, and Excel report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ventus-z](https://clawhub.ai/user/ventus-z) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and test engineers use this skill to create and operate a gRPC and JMeter workflow for validating C/C++ SDKs on embedded boards. It supports SDK header analysis, proto and server wrapper guidance, board deployment steps, test execution, and report generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill documents unauthenticated board-control and plaintext gRPC services. <br>
Mitigation: Bind services to localhost or an isolated lab network, and add authentication, TLS, or firewall rules before using them outside a controlled test environment. <br>
Risk: The workflow includes remote upload, execution, service control, and a shutdown command for embedded boards. <br>
Mitigation: Review generated scripts before execution, run with least required privileges, and disable or avoid shutdown behavior unless explicitly required. <br>
Risk: Some scripts automatically install Python packages. <br>
Mitigation: Run the workflow in a virtual environment or container with reviewed and pinned dependencies. <br>
Risk: Generated reports may contain SDK, device, request, response, or error details. <br>
Mitigation: Store reports in controlled locations and clean them up when they are no longer needed. <br>


## Reference(s): <br>
- [SDK Analysis Guide](references/sdk-analysis.md) <br>
- [C++ gRPC Server Implementation Guide](references/cpp-server.md) <br>
- [Serial Communication Protocol](references/serial-protocol.md) <br>
- [JMeter gRPC Plugin Configuration](references/jmeter-config.md) <br>
- [JMX Test Plan Template](references/jmx-template.md) <br>
- [Protocol Buffer Design](references/proto-design.md) <br>
- [Test Patterns](references/test-patterns.md) <br>
- [Excel Report Format](references/excel-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with code blocks, shell commands, generated project files, JMX XML, proto definitions, and Excel report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local project scaffolds and test reports when its scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
