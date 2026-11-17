## Description:

Omada Viewer provides read-only diagnostics for TP-Link Omada SDN controllers via the Open API, covering devices, clients, VLANs, LAN networks, WAN status, router and switch ports, DHCP ranges, port forwards, and controller health.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imjuff](https://clawhub.ai/user/imjuff)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, network administrators, and support engineers use Omada Viewer to inspect Omada inventory and network health during troubleshooting without making configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Omada Open API credentials and can expose network inventory and client metadata.

Mitigation: Use a dedicated Viewer-only Open API application, store credentials locally, and do not paste secrets into chat.

Risk: Disabling TLS certificate verification can expose credentials or controller data to interception.

Mitigation: Keep certificate verification enabled and do not set OMADA_VERIFY_SSL=false unless the environment has been separately secured.

Risk: The bundled endpoint catalog includes write-capable Omada API references even though the skill is framed for read-only diagnostics.

Mitigation: Limit use to read-only diagnostic commands and do not use the broad endpoint catalog for write or administrator operations.

## Reference(s):

- [Omada Viewer release page](https://clawhub.ai/imjuff/skills/omada-viewer)
- [Omada Northbound API Endpoints Reference](references/api-endpoints.md)
- [Practical Omada Endpoints](references/discovered-endpoints.md)
- [Omada Controller API Endpoints](references/all-endpoints.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and optional table or JSON command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May query a user-configured Omada controller using supplied Open API credentials for read-only diagnostics.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
