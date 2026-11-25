## Description:

Set up, use, refresh, or troubleshoot Hashference as an OpenClaw inference provider, including secure sign-in, live model discovery, protocol routing, model selection, fallbacks, and subagents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mpoletiek](https://clawhub.ai/user/mpoletiek)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to connect and manage Hashference inference routes. It guides secret-safe setup, current model discovery, provider registration, routing choices, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Provider setup and account operations may involve credentials, configuration changes, and paid inference.

Mitigation: Use the host-approved masked-entry or SecretRef workflow; review the exact provider, routing, model, and price before authorizing changes or paid calls.

## Reference(s):

- [Hashference model catalog](https://hashference.com/v1/catalog)
- [Hashference capabilities](https://hashference.com/v1/capabilities)
- [OpenClaw custom providers](https://docs.openclaw.ai/concepts/model-providers/custom-providers)
- [Setup guidance](references/setup.md)
- [Model discovery and selection](references/models.md)
- [Security boundaries](references/SECURITY.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown guidance, shell commands, JSON model catalogs, and OpenClaw model registration fragments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Catalog inventory, prices, privacy details, and model limits can change; refresh live data before setup or paid use.]

## Skill Version(s):

1.0.1 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
