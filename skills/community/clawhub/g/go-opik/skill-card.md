## Description:

Unofficial Go client for the Opik REST API, generated with oapi-codegen from the specification Comet publishes. Package opik (github.com/psyb0t/go-opik) has typed methods for projects, traces, spans, datasets, experiments, prompts, feedback scores, annotation queues and the other published endpoints. Use when Go code needs Opik LLM observability data or already imports go-opik.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT

## Use Case:

Developers use this skill to install and work with the unofficial typed Go client for Opik, including configuring authentication and making API calls for projects, traces, spans, datasets, experiments, prompts, and evaluation feedback.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opik API credentials could be exposed if they are hardcoded, committed, or included in logs.

Mitigation: Read the API key and workspace from OPIK_API_KEY and OPIK_WORKSPACE, and do not log credentials or request headers.

Risk: Trace and span payloads may contain prompts, model output, or other sensitive data, and API calls can send, update, or delete remote data.

Mitigation: Use the selected Opik destination and send, update, or delete data only for the action requested by the user.

Risk: The security scan could not resolve one reference, so the available scan coverage is incomplete.

Mitigation: Review the unresolved reference when deciding whether to install, as advised by the server security guidance.

## Reference(s):

- [Setup and reference](references/setup.md)
- [Go package documentation](https://pkg.go.dev/github.com/psyb0t/go-opik)
- [Project repository](https://github.com/psyb0t/go-opik)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration instructions, API calls]

**Output Format:** [Markdown with Go code blocks and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Go examples for API requests, authentication, and client configuration.]

## Skill Version(s):

0.5.0 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
