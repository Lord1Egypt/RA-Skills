## Description: <br>
Starts a local mock HTTP server from an OpenAPI 3.x or Swagger 2.0 spec, using Stoplight Prism to validate the spec and generate example endpoint responses. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[PHY041](https://clawhub.ai/user/PHY041) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, frontend teams, and API testers use this skill to turn a trusted OpenAPI or Swagger spec into a local mock server for contract-first development, integration testing, and backend-independent frontend work. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may ask an agent to run Prism through npm, npx, or Docker and start a localhost server. <br>
Mitigation: Review commands before execution, prefer trusted package or image sources, bind the server to localhost, and stop the server when testing is complete. <br>
Risk: Untrusted local filenames or remote OpenAPI specs can lead to misleading mock responses or unsafe command inputs. <br>
Mitigation: Use trusted local specs or trusted HTTPS URLs, and inspect unfamiliar specs before using them to start a mock server or generate test commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/PHY041/phy-openapi-mock-server) <br>
- [Canlah AI homepage](https://canlah.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash, Python, curl, Docker, YAML, and environment configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local-server startup guidance, endpoint inventory, test curl commands, troubleshooting notes, and OpenAPI example-authoring guidance.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
