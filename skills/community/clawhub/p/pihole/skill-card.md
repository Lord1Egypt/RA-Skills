## Description:

Control a Pi-hole v6 DNS ad blocker through its API to check status, view statistics, enable or disable blocking, and inspect blocked domains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[baanish](https://clawhub.ai/user/baanish)

### License/Terms of Use:


## Use Case:

Developers, operators, and homelab administrators use this skill to manage a configured Pi-hole instance from an agent workflow. It supports routine DNS blocking checks, temporary enable or disable actions, and blocked-domain analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports credential-handling concerns, including avoiding exposure through process arguments or plaintext transport.

Mitigation: Use an explicitly configured Pi-hole URL over HTTPS with a valid certificate, protect the API token in configuration or environment storage, and avoid insecure mode except on tightly controlled networks.

Risk: The security evidence says timed disables should remain timed and recommends verifying Pi-hole status after disable commands.

Mitigation: Prefer short timed disable operations, verify blocking status after each disable action, and review the script before broad deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/baanish/skills/pihole)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text status output with Markdown-style setup examples and shell-backed Pi-hole API operations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a configured Pi-hole API URL and app password, plus curl and jq; operations can change DNS blocking state.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
