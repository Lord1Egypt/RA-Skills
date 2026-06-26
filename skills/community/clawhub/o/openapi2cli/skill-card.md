## Description: <br>
Generate CLI tools from OpenAPI specs. Built for AI agents who hate writing curl commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[awlevin](https://clawhub.ai/user/awlevin) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI agents use this skill to generate command-line clients from OpenAPI or Swagger specifications, making APIs easier to inspect, call, and chain from shell workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated CLIs may require API credentials and can expose secrets if keys are passed directly as command-line flags. <br>
Mitigation: Prefer environment variables or a secret manager for credentials and avoid placing secret values in shell history. <br>
Risk: Generated CLIs make real API calls and may mutate production resources. <br>
Mitigation: Inspect generated commands before running them, use staging or test APIs when possible, and get explicit confirmation before mutating production resources. <br>
Risk: Generated clients inherit behavior from the OpenAPI specification and may produce commands that do not match user intent. <br>
Mitigation: Review generated commands and use dry-run inspection when available before executing API operations. <br>


## Reference(s): <br>
- [OpenAPI to CLI on ClawHub](https://clawhub.ai/awlevin/openapi2cli) <br>
- [openapi2cli on PyPI](https://pypi.org/project/openapi2cli/) <br>
- [openapi2cli GitHub project](https://github.com/Olafs-World/openapi2cli) <br>


## Skill Output: <br>
**Output Type(s):** [Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash examples and generated CLI files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated CLIs can emit structured JSON responses and support dry-run inspection when the underlying tool is used that way.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
