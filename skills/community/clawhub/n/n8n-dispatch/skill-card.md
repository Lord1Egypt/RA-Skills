## Description:

Forwards state, action, or historical user requests to a configured n8n_dispatch MCP service and returns the service response.

This skill is ready for commercial/non-commercial use.

## Publisher:

[enchantedmotorcycle](https://clawhub.ai/user/enchantedmotorcycle)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to connect OpenClaw commands with an n8n workflow for home-automation state checks, actions, and historical queries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can forward action requests and home-automation details to an n8n workflow.

Mitigation: Use it only with an n8n workflow you control, add authentication and least-privilege checks in n8n, and avoid sending secrets or sensitive household details.

Risk: The artifact shows unsafe transport guidance and weak input scoping for dispatch payloads.

Mitigation: Prefer HTTPS or local-only loopback, validate requestType, and build JSON payloads with a real serializer before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/enchantedmotorcycle/skills/n8n-dispatch)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text responses with shell command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Dispatch requests include a requestType value and user prompt text.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
