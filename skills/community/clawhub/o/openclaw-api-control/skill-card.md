## Description:

Control a hosted OpenClaw instance through the OpenClaw as a Service API for chat, file transfer, workspace file access, command execution, hosted instance management, and API-key based agent integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fstandhartinger](https://clawhub.ai/user/fstandhartinger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to operate a hosted OpenClaw instance through API calls, including sending chat messages, transferring files, reading and writing workspace files, running terminal commands, and managing instances.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key grants broad remote-control powers over OpenClaw instances owned by the authenticated user.

Mitigation: Install only when remote administrative control is needed, trust the publisher, and use a limited-scope API key if available.

Risk: A custom OPENCLAW_API_BASE_URL can receive the API key and uploaded local files.

Mitigation: Keep OPENCLAW_API_BASE_URL set to the official HTTPS endpoint unless the alternative server is fully trusted.

Risk: The upload-tree action can transmit local project files, including sensitive text files, to the remote OpenClaw instance.

Mitigation: Avoid upload-tree on broad directories containing .env files, keys, tokens, or private project data.

## Reference(s):

- [OpenClaw API Control on ClawHub](https://clawhub.ai/fstandhartinger/skills/openclaw-api-control)
- [fstandhartinger ClawHub Publisher Profile](https://clawhub.ai/user/fstandhartinger)
- [OpenClaw as a Service API endpoint](https://openclaw-as-a-service.com/api)
- [scripts/openclaw_api_client.mjs](scripts/openclaw_api_client.mjs)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The helper prints machine-readable JSON for most API actions and streams chat output when requested.]

## Skill Version(s):

0.1.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
