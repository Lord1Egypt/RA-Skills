## Description:

Monitor and manage Dell PowerEdge servers through the iDRAC Redfish API for hardware status, health, inventory, logs, thermal data, storage details, and power-state checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddygk](https://clawhub.ai/user/eddygk)

### License/Terms of Use:


## Use Case:

Developers and infrastructure operators use this skill to inspect and manage Dell PowerEdge server health and inventory through user-configured iDRAC endpoints. It can also help prepare shell commands for Redfish API operations that require careful review before execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses out-of-band server management APIs that can expose sensitive hardware state or affect server availability.

Mitigation: Use a least-privileged iDRAC account and review any proposed management or power-operation command before execution.

Risk: TLS verification is disabled for iDRAC HTTPS calls, which can allow interception if the management network is not trusted.

Mitigation: Prefer trusted certificates or certificate pinning and avoid production use with curl -k unless the network and endpoint identity are controlled.

Risk: Credentials may be cached in a local plaintext file.

Mitigation: Avoid caching 1Password or environment credentials into plaintext files when possible, enforce mode 600, and rotate credentials if local exposure is suspected.

Risk: The configuration file is sourced as shell code.

Mitigation: Inspect the configuration file before use and restrict write access to the user account running the skill.

## Reference(s):

- [iDRAC Redfish API Endpoint Reference](references/endpoints.md)
- [DMTF Redfish Specification](https://www.dmtf.org/standards/redfish)
- [Dell iDRAC Redfish Scripting](https://github.com/dell/iDRAC-Redfish-Scripting)
- [iDRAC Skill on ClawHub](https://clawhub.ai/eddygk/skills/idrac)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that access user-configured iDRAC endpoints and parse Redfish JSON responses with jq.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
