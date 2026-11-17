## Description:

Deploy an API gateway management system with four agents for service discovery, routing, authentication, and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and platform engineers use this skill to set up a Pilot API gateway deployment with separate discovery, router, auth, and monitor agents. It helps coordinate service registry updates, request routing, credential checks, rate limiting, access logs, health feedback, and alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad setup commands can install dependent skills and write Pilot setup manifests in the user's environment.

Mitigation: Review the skill before installation, pin and verify each installed skill, and inspect the generated manifest before writing it.

Risk: Deployment prefixes are used to form hostnames and handshake targets.

Mitigation: Validate the prefix as a simple hostname label before running hostname or handshake commands.

Risk: Example API keys, bearer tokens, customer identifiers, and access logs may be copied into demo or Slack flows.

Mitigation: Use only test credentials and redacted operational data when exercising publish, logging, dashboard, or Slack alert flows.

Risk: The skill coordinates multiple agents across a Pilot API gateway setup.

Mitigation: Use it only in a controlled Pilot environment with expected peers and verified trust handshakes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/teoslayer/skills/pilot-api-gateway-manager-setup)
- [Pilot Protocol homepage](https://pilotprotocol.network)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Role-specific setup manifests, hostname commands, skill installation commands, and peer handshake guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
