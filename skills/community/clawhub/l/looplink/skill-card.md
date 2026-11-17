## Description:

Interact with looplink (looplink.app) - A social content organizer / bookmarking app

This skill is ready for commercial/non-commercial use.

## Publisher:

[sleep9](https://clawhub.ai/user/sleep9)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to connect an agent to Looplink's social content organizer through its MCP manifest and tool execution endpoints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives a remote service broad, changing tool authority through a dynamically loaded MCP manifest.

Mitigation: Install only if the publisher and Looplink service are trusted, and review the manifest's available tools and authorization requirements before enabling agent access.

Risk: The skill uses a permanent apiKey that functions as a long-lived agent credential.

Mitigation: Store the apiKey in a secure secret store, avoid logging or exposing it, and confirm that it can be revoked or rotated if the agent or device is compromised.

## Reference(s):

- [Looplink MCP manifest endpoint](https://api.looplink.app/mcp/manifest)
- [Looplink MCP tool execution endpoint](https://api.looplink.app/mcp/call)
- [ClawHub skill page](https://clawhub.ai/sleep9/skills/looplink)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Configuration, Guidance]

**Output Format:** [Structured JSON responses and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require a permanent Looplink apiKey for authorized tools.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
