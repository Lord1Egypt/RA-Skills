## Description:

设计自动化的工作流程，以节省时间，提供工作效率，通过本技能自动识别设计的工作流，触发对应的工作流，实现流程自动化

This skill is ready for commercial/non-commercial use.

## Publisher:

[somta](https://clawhub.ai/user/somta)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workflow operators use this skill to trigger configured Juggle workflows, pass workflow parameters, poll asynchronous executions, and retrieve workflow results through the Juggle OpenAPI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger external Juggle workflows with a token and user-supplied data.

Mitigation: Install only when you control the Juggle endpoint and token, and confirm the workflow key, version, and parameters before execution.

Risk: Workflow data passed on the command line can include sensitive values and may appear in shell history or process logs.

Mitigation: Avoid passing passwords or other secrets through --flow-data, and scope the Juggle token to only the workflows required.

Risk: An untrusted or plain HTTP base URL could expose workflow data or tokens.

Mitigation: Use an HTTPS trusted MC_JUGGLE_BASE_URL before running workflow commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/somta/skills/juggle)
- [Juggle quick start documentation](https://juggle.plus/docs/guide/start/quick-start/)
- [API specification](artifact/references/api_spec.md)
- [Workflow specification](artifact/references/flow_spec.md)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [CLI text with JSON API responses and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires MC_JUGGLE_BASE_URL and MC_JUGGLE_TOKEN; asynchronous workflows can be polled automatically or queried manually by flow instance ID.]

## Skill Version(s):

1.0.0 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
