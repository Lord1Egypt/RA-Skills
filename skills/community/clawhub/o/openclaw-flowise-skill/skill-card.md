## Description:

Interact with Flowise AI workflows via REST API. Use when user mentions Flowise, chatflows, or wants to send messages to Flowise bots/agents. Supports listing flows, sending predictions, and managing conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tianmu](https://clawhub.ai/user/tianmu)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to connect an agent to configured Flowise chatflows, list available flows, retrieve flow details, send prediction requests, and maintain conversation sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, uploaded files, flow metadata, session identifiers, and API credentials may be sent to a user-configured Flowise server.

Mitigation: Install only when the configured Flowise server is trusted, prefer HTTPS for non-local endpoints, and avoid sending sensitive data unless the workflow is approved for that data.

Risk: API keys may be exposed if stored in shared project files or shell history.

Mitigation: Use least-privilege credentials and keep live API keys out of shared files and command history.

Risk: Some Flowise workflows may accept script or device form inputs that can cause actions on other systems.

Mitigation: Use script/device form flows only when that behavior is intentional and the target system is authorized.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tianmu/skills/openclaw-flowise-skill)
- [Publisher profile](https://clawhub.ai/user/tianmu)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON examples, shell commands, and optional JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Flowise flow identifiers, session identifiers, API request examples, and parsed Flowise response data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
