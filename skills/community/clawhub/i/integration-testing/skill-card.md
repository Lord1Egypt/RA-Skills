## Description: <br>
Automated integration testing with external services using testcontainers, wiremock, localstack. Use when developer needs to set up integration tests for testing with real services in Docker containers via testcontainers, mocking HTTP APIs with WireMock, testing AWS S3 with LocalStack, SFTP integration testing, or setting up complex integration test environments with external dependencies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ahmed181283](https://clawhub.ai/user/ahmed181283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to set up isolated integration tests with Docker-based services, mocked HTTP APIs, LocalStack S3, and SFTP test environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can install or execute external software. <br>
Mitigation: Review scripts before running them, verify downloaded or installed dependencies, and execute them only in an isolated development environment. <br>
Risk: Helper scripts can persist environment changes in a shell profile. <br>
Mitigation: Keep AWS and Testcontainers variables scoped to a project or one terminal session, and avoid allowing scripts to modify ~/.bashrc unless the change is intentional. <br>
Risk: Disabling Testcontainers cleanup can leave containers running after tests. <br>
Mitigation: Remove TESTCONTAINERS_RYUK_DISABLED unless persistent containers are intentionally needed, and clean up local Docker resources after testing. <br>


## Reference(s): <br>
- [Testcontainers Guide](references/testcontainers-guide.md) <br>
- [WireMock Patterns](references/wiremock-patterns.md) <br>
- [LocalStack S3 Configuration Guide](references/localstack-s3-config.md) <br>
- [Security & Compliance](SECURITY.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with Python examples, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes helper scripts and templates for local integration-test environments] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
