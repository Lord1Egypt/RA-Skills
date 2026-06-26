## Description: <br>
MockLab is an intelligent API toolbox that helps agents turn API documents into mock schemas, start a local mock server, forward requests, reproduce data, and support interface development and debugging. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lancer07](https://clawhub.ai/user/lancer07) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, QA engineers, and integration teams use this skill to create local mock APIs from interface documentation, simulate realistic responses, forward requests to local services, and reproduce test data while backend or third-party environments are unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs a local API debugging server with unauthenticated control endpoints. <br>
Mitigation: Run it only on a trusted machine or container and avoid exposing port 18080 to other devices. <br>
Risk: The request forwarding feature can send traffic to arbitrary target URLs. <br>
Mitigation: Use test credentials only, proxy only to trusted local or controlled endpoints, and avoid forwarding sensitive production data. <br>
Risk: Generated schemas and persisted state may contain secrets or sensitive test data. <br>
Mitigation: Review exported schemas and state files before sharing or committing them. <br>


## Reference(s): <br>
- [MockLab ClawHub listing](https://clawhub.ai/lancer07/mocklab) <br>
- [Schema template reference](references/demo.json) <br>
- [Actual generated response examples](references/demo__实际返回示例.json) <br>
- [Field key naming rules](references/field_keys.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON schema/configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create project schema JSON files, run a local mock API server, and guide use of a localhost web UI.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
