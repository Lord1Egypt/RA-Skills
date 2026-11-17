## Description:

Bridge GitHub webhook events into Pilot Protocol so agents can react to repository events.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure a GitHub webhook bridge that forwards repository events into Pilot Protocol, enabling Pilot agents to trigger CI/CD, review, or automation workflows from push and pull request events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A public or unauthenticated GitHub webhook relay could let untrusted events reach Pilot agents.

Mitigation: Deploy the relay privately or behind authentication and require GitHub webhook signature verification before forwarding events.

Risk: Webhook payloads can trigger downstream build or review agents without sufficient validation.

Mitigation: Validate event schema and source, use repository and branch allowlists, and route events only to least-privilege downstream agents.

Risk: Repeated or replayed webhook deliveries could cause duplicate or excessive automation actions.

Mitigation: Add replay protection, idempotency checks, and rate limiting before acting on received webhook events.

## Reference(s):

- [Pilot Protocol homepage](https://pilotprotocol.network)
- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-github-bridge)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands assume pilotctl, a running Pilot daemon, GitHub webhooks, gh CLI, and an HTTP relay server are available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
