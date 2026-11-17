## Description:

Mxchip Smart Control lets agents query and control Smart Plus smart-home devices, air conditioners, and scenes through the MXCHIP MCP service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mxchipyun](https://clawhub.ai/user/mxchipyun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent query Smart Plus devices and scenes, turn supported devices on or off, adjust air-conditioner settings, and trigger configured automation scenes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can immediately control physical smart-home devices and scenes.

Mitigation: Require explicit user confirmation before turning devices on or off, changing air-conditioner settings, or triggering scenes.

Risk: The MXCHIP_OAUTH_TOKEN credential grants access to Smart Plus devices.

Mitigation: Keep the token secret, store it only in the environment or an approved secret store, and rotate it if exposed.

Risk: The token-bearing client accepts a custom base URL.

Mitigation: Use the official MXCHIP endpoint unless an alternate endpoint has been independently validated.

Risk: The dependency declaration is not pinned to an exact version.

Mitigation: Prefer a pinned dependency set before production deployment.

## Reference(s):

- [Mxchip Smart Control API Reference](references/api_reference.md)
- [MXCHIP Official Website](https://www.mxchip.com/)
- [MXCHIP OAuth Token Endpoint](https://app.api.cloud.mxchip.com:2443/oauth2/mcp/oauth)
- [MXCHIP MCP Endpoint](https://app.api.cloud.mxchip.com:2443/mcp)
- [ClawHub Skill Listing](https://clawhub.ai/mxchipyun/skills/mxchip-smart-control)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses JSON-RPC 2.0 over HTTP and requires MXCHIP_OAUTH_TOKEN for authenticated API calls.]

## Skill Version(s):

1.0.2 (source: skill.json, README.md, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
