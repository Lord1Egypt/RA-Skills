## Description:

Gates persona sharing behind explicit Telegram owner approval and connects to persona-service for external chatbots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kanishkarandunu](https://clawhub.ai/user/kanishkarandunu)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to require explicit Telegram owner consent before an agent shares local persona, profile, identity, writing-style, or system-personality content. It can also connect to a persona-service flow so external chatbots can request persona access through the same approval gate.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approved persona content, request metadata, and optional shared secrets can leave the machine through the configured persona-service endpoint.

Mitigation: Install only with trusted HTTPS persona-service endpoints, use a dedicated Telegram bot token, and restrict permissions on OpenClaw configuration files.

Risk: The persona-service client can run as a detached background process with weak endpoint and environment scoping.

Mitigation: Be prepared to stop the persona-client process manually, and prefer a version that validates endpoints, allowlists child-process environment variables, validates numeric backoff settings, and ties the client lifecycle to the gateway.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kanishkarandunu/skills/persona-consent-telegram-hub)
- [README](README.md)
- [End-to-end test guide](docs/E2E-TEST.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown or refusal text, with JSON returned by the local consent script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns persona Markdown only after approval; denies by default on timeout, error, or refusal.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
