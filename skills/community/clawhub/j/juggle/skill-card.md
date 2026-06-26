## Description: <br>
Triggers Juggle workflows through OpenAPI, passes workflow parameters, and retrieves synchronous or asynchronous execution results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[somta](https://clawhub.ai/user/somta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to trigger configured Juggle workflow processes, pass JSON input data, poll asynchronous runs, and inspect execution results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start external Juggle automations with a token, including workflows that may affect accounts, business data, production systems, payments, or public content. <br>
Mitigation: Review workflow definitions and token permissions before installation, use a least-privilege token, and require explicit confirmation before high-impact workflow execution. <br>
Risk: Flow input data may contain sensitive values and can be exposed if placed directly in command lines, examples, or logs. <br>
Mitigation: Avoid putting real secrets in flow-data command arguments or documentation, and route secrets through approved credential handling. <br>


## Reference(s): <br>
- [Juggle Quick Start](https://juggle.plus/docs/guide/start/quick-start/) <br>
- [Juggle API Specification](references/api_spec.md) <br>
- [Juggle Workflow Specification](references/flow_spec.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API calls, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires MC_JUGGLE_BASE_URL and MC_JUGGLE_TOKEN; asynchronous workflows poll for completion by default.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
